#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from datetime import datetime, timedelta

from django.contrib.sessions.models import Session
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.settings import api_settings
from rest_framework.renderers import XMLRenderer
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from cart.base.basecartcontroller import BaseCartController
from cart.dalliz.dallizcartcontroller import DallizCartController
from cart.models import MetaCart

from auchan.models import History as AuchanHistory, Product as AuchanProduct, Promotion as AuchanPromotion

from dalliz.models import Category

from monoprix.models import History as MonoprixHistory, Product as MonoprixProduct, Promotion as MonoprixPromotion

from ooshop.models import History as OoshopHistory, Product as OoshopProduct, Promotion as OoshopPromotion

from api.renderer import ProductsCSVRenderer, ProductRecommendationCSVRenderer, NewProductsCSVRenderer
from api.serializer.dalliz.serializer import CategorySerializer
from api.serializer.auchan.serializer import ProductSerializer as AuchanProductSerializer, CartContentSerializer as AuchanCartContentSerializer
from api.serializer.auchan.serializer import RecommendationSerializer as AuchanRecommendationSerializer
from api.serializer.monoprix.serializer import ProductSerializer as MonoprixProductSerializer, CartContentSerializer as MonoprixCartContentSerializer
from api.serializer.monoprix.serializer import RecommendationSerializer as MonoprixRecommendationSerializer
from api.serializer.ooshop.serializer import ProductSerializer as OoshopProductSerializer
from api.serializer.ooshop.serializer import RecommendationSerializer as OoshopRecommendationSerializer, CartContentSerializer as OoshopCartContentSerializer

AVAILABLE_OSMS = [
	{
		'name':'monoprix',
		'type':'shipping',
	},{
		'name':'ooshop',
		'type':'shipping',
	},{
		'name':'auchan',
		'type':'shipping',
	}
]

def osm(function):
	"""
		This decorator gets osm arguments from request
	"""
	def wrapper( self , *args, **kwargs):
		# Looking for request object
		for element in args:
			if isinstance(element, Request):
				# Found it
				request = element
				break

		# Default osm
		osm = {
			'name':'monoprix',
			'type':'shipping',
			'location':None
		}
		if request.method in ['GET', 'POST']:
			parameters = getattr(request, request.method)
			if 'osm_name' in parameters:
				osm['name'] = parameters['osm_name']
			if 'osm_type' in parameters:
				osm['type'] = parameters['osm_type']
			if 'osm_location' in parameters:
				osm['location'] = parameters['osm_location']

		# Getting session information
		session_key = request.session.session_key
		if session_key is None:
			request.session.set_test_cookie()
		else:
			if request.session.test_cookie_worked():
				request.session.delete_test_cookie()
				print 'Test cookie set correctly, removing it!'

		# Getting metacart
		metacart = None
		if session_key is not None:
			metacart = MetaCart.objects.filter(session__session_key = session_key)
			if len(metacart)>0:
				metacart = metacart[0]
			else:
				metacart = MetaCart(session = Session.objects.get(session_key = session_key))
				metacart.save()

		# Setting cart
		cart_controller = DallizCartController(osm = osm['name'], metacart = metacart)
		request.cart_controller = cart_controller

		carts = { o: {
			'id': cart_controller.carts[o].cart.id,
			'price':  (lambda x: x.cart.cart_history_set.all()[0].price if len(x.cart.cart_history_set.all())>0 else 0)(cart_controller.carts[o]),
			'created': (lambda x: x.cart.cart_history_set.all()[0].created if len(x.cart.cart_history_set.all())>0 else None)(cart_controller.carts[o]),
		}
			for o in cart_controller.carts
		}

		kwargs.update(dict([ ( 'osm_%s'%k , v) for k,v in osm.iteritems()]))

		data = function( self , *args, **kwargs)

		if isinstance(data, dict):
			data.update({'osm': osm})
			if 'carts' not in data:
				data.update({'carts': carts})
			return Response(data)
		else:
			return data
	return wrapper

class BaseAPIView(APIView):
    """
	    Base Api view for dalliz api.
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [XMLRenderer]

class CategoryAll(BaseAPIView):
	"""
		View for all category.
	"""
	@osm
	def get(self, request, format=None,**kwargs):
		data = CategorySerializer.all()
		return {'categories':data}


class CategorySimple(BaseAPIView):
	"""
		Get single category view.
	"""
	def get_object(self, id_category):
		try:
			return Category.objects.get(id=id_category)
		except Category.DoesNotExist:
			raise Http404
	@osm
	def get(self, request, id_category,**kwargs):
		category = self.get_object(id_category)
		subs = CategorySerializer.all(category)
		data = CategorySerializer(category).data
		data.update({'subs': subs})
		if data is None:
			return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
		else:
			return {'category':data}

class CategoryProducts(CategorySimple):
	"""
		Get products for a category
	"""
	TOP_PRODUCTS_COUNT = 5
	MID_PRODUCTS_COUNT = 11
	renderer_classes = BaseAPIView.renderer_classes + [ProductsCSVRenderer]
	@osm
	def get(self, request, id_category, key, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		category = self.get_object(id_category)
		serialized = None
		global_keys = globals().keys()

		# Settings location kwargs :
		kwargs_location_history = {}
		kwargs_location_promotion = {}
		if osm_name == 'monoprix':
			if osm_location is None:
				kwargs_location_history['history__store__isnull'] = True
				kwargs_location_promotion['store__isnull'] = True
			else:
				kwargs_location_history['history__store__id'] = osm_location
				kwargs_location_promotion['store__id'] = osm_location
		else:
			if osm_location is None:
				kwargs_location_history['history__shipping_area__isnull'] = True
				kwargs_location_promotion['shipping_area__isnull'] = True
			else:
				kwargs_location_history['history__shipping_area__id'] = osm_location
				kwargs_location_promotion['shipping_area__id'] = osm_location

		# Getting products without simple promotion
		product_class_name = '%sProduct'%osm_name.capitalize()
		if product_class_name in global_keys:
			Product = globals()[product_class_name]
			kwargs = {
				'exists':True,
				'dalliz_category': category
			}
			kwargs.update(kwargs_location_history) # adding location filter


			products = Product.objects.filter(**kwargs).distinct('reference')
			products_count = products.count() # Adding total count of products in category
			if key == 'top':
				products = products[:CategoryProducts.TOP_PRODUCTS_COUNT]
			elif key == 'mid':
				products = products[CategoryProducts.TOP_PRODUCTS_COUNT:CategoryProducts.MID_PRODUCTS_COUNT]
			elif key == 'end':
				products = products[CategoryProducts.MID_PRODUCTS_COUNT:]

		serializer_class_name = '%sProductSerializer'%osm_name.capitalize()
		cart = getattr(request.cart_controller.metacart, osm_name+'_cart')

		if serializer_class_name in global_keys:
			Serializer_class = globals()[serializer_class_name]
			serialized = Serializer_class(products, many = True, context = {'osm': {'name':osm_name,'type': osm_type, 'location':osm_location}, 'time':datetime.now(), 'cart': cart})
		if serialized is None:
			return Response(404, status=status.HTTP_400_BAD_REQUEST)
		else:
			return {'products':serialized.data, 'category':{'name': category.name, 'count': products_count}}

class CategoryMatching(CategorySimple):
	"""
		Get recommendation for product
	"""
	renderer_classes = BaseAPIView.renderer_classes + [ProductRecommendationCSVRenderer]

	@osm
	def get(self, request, id_category, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		category = self.get_object(id_category)
		serialized = None
		global_keys = globals().keys()
		product_class_name = '%sProduct'%osm_name.capitalize()
		if product_class_name in global_keys:
			Product = globals()[product_class_name]
			kwargs = {
				'exists':True,
				'dalliz_category': category
			}

			if osm_name == 'monoprix':
				if osm_location is None:
					kwargs['history__store__isnull'] = True
				else:
					kwargs['history__store__id'] = osm_location
			else:
				if osm_location is None:
					kwargs['history__shipping_area__isnull'] = True
				else:
					kwargs['history__shipping_area__id'] = osm_location

			products = Product.objects.filter(**kwargs).distinct('reference')

		serializer_class_name = '%sProductSerializer'%osm_name.capitalize()
		
		if serializer_class_name in global_keys:
			global_keys = globals().keys()
			serialized = []
			# Processing matching
			for product in products:
				Serializer_class = globals()[serializer_class_name]
				serialized_product = Serializer_class(product, context = {'osm': {'name':osm_name,'type': osm_type, 'location':osm_location}}).data
				matching = product.productmatch_set.all()
				if len(matching)>0:
					matching = matching[0]
					for osm in AVAILABLE_OSMS:
						match = getattr(matching, '%s_product'%osm['name'])
						if match is not None and osm['name'] != osm_name:
							serializer_class_name_match = '%sProductSerializer'%osm['name'].capitalize()
							# print osm['name']
							Serializer = globals()[serializer_class_name_match]
							serialized_product[osm['name']] = Serializer(match, context = {'osm': {'name':osm['name'],'type': osm_type, 'location':osm_location}}).data
						elif osm['name'] != osm_name:
							serialized_product[osm['name']] = {}
				else:
					for osm in AVAILABLE_OSMS:
						if osm['name'] != osm_name:
							serialized_product[osm['name']] = {}


				serialized.append(serialized_product)


		if serialized is None:
			return Response(404, status=status.HTTP_400_BAD_REQUEST)
		else:
			return {'products':serialized}

class NewProducts(BaseAPIView):
	"""
		API view for extracting new products (created in the last 7 days)
	"""
	renderer_classes = BaseAPIView.renderer_classes + [NewProductsCSVRenderer]

	@osm
	def get(self, request, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		serialized = None
		global_keys = globals().keys()
		product_class_name = '%sProduct'%osm_name.capitalize()
		if product_class_name in global_keys:
			Product = globals()[product_class_name]
			kwargs = {
				'exists':True,
				'created__gte': datetime.now()-timedelta(days = 5)
				# 'html__isnull': True
			}

			if osm_name == 'monoprix':
				if osm_location is None:
					kwargs['history__store__isnull'] = True
				else:
					kwargs['history__store__id'] = osm_location
			else:
				if osm_location is None:
					kwargs['history__shipping_area__isnull'] = True
				else:
					kwargs['history__shipping_area__id'] = osm_location

			products = Product.objects.filter(**kwargs)

		serializer_class_name = '%sProductSerializer'%osm_name.capitalize()
		
		if serializer_class_name in global_keys:
			global_keys = globals().keys()
			serialized = []
			# Processing matching
			for product in products:
				Serializer_class = globals()[serializer_class_name]
				serialized_product = Serializer_class(product, context = {'osm': {'name':osm_name,'type': osm_type, 'location':osm_location}}).data
				matching = product.productmatch_set.all()
				if len(matching)>0:
					matching = matching[0]
					for osm in AVAILABLE_OSMS:
						match = getattr(matching, '%s_product'%osm['name'])
						if match is not None and osm['name'] != osm_name:
							serializer_class_name_match = '%sProductSerializer'%osm['name'].capitalize()
							# print osm['name']
							Serializer = globals()[serializer_class_name_match]
							serialized_product[osm['name']] = Serializer(match, context = {'osm': {'name':osm['name'],'type': osm_type, 'location':osm_location}}).data
						elif osm['name'] != osm_name:
							serialized_product[osm['name']] = {}
				else:
					for osm in AVAILABLE_OSMS:
						if osm['name'] != osm_name:
							serialized_product[osm['name']] = {}


				serialized.append(serialized_product)


		if serialized is None:
			return Response(404, status=status.HTTP_400_BAD_REQUEST)
		else:
			return {'products':serialized}

class Product(BaseAPIView):
	"""
		API view for a product.
	"""

	def get_object(self, reference, osm_name):
		
			global_keys = globals().keys()
			product_class_name = '%sProduct'%osm_name.capitalize()

			if product_class_name in global_keys:
				Product = globals()[product_class_name]
				try:
					return Product.objects.get(reference = reference)
				except Product.DoesNotExist:
					raise Http404
			else:
				raise Http404


	@osm
	def get(self, request, reference, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		product = self.get_object(reference, osm_name)
		global_keys = globals().keys()
		serialized = None
		serializer_class_name = '%sProductSerializer'%osm_name.capitalize()
		if serializer_class_name in global_keys:
			Serializer = globals()[serializer_class_name]
			serialized = Serializer(product, context = {'osm': {'name':osm_name,'type': osm_type, 'location':osm_location}})

		if serialized is None:
			return Response(404, status=status.HTTP_400_BAD_REQUEST)
		else:
			return {'product':serialized.data}

class ProductRecommendation(Product):
	"""
		Get Recommendation for product
	"""
	# renderer_classes = BaseAPIView.renderer_classes + [ProductRecommendationCSVRenderer]

	@osm
	def get(self, request, reference, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		product = self.get_object(reference, osm_name)
		global_keys = globals().keys()
		serialized = None
		recommendations = {}
		osm_recommendation = [ osm['name'] for osm in AVAILABLE_OSMS if osm['name'] != osm_name]

		# Processing matching
		matching = product.productmatch_set.all()
		if len(matching)>0:
			matching = matching[0]
			for osm in AVAILABLE_OSMS:
				match = getattr(matching, '%s_product'%osm['name'])
				if match is not None and osm['name'] != osm_name and osm['name'] in osm_recommendation:
					serializer_class_name = '%sRecommendationSerializer'%osm['name'].capitalize()
					Serializer = globals()[serializer_class_name]
					recommendations[osm['name']] = [ Serializer(match, context = { 'matching': True}).data]
					osm_recommendation.remove(osm['name'])

		# Processing recommendation
		for osm in osm_recommendation:
			if osm != osm_name:
				serializer_class_name = '%sRecommendationSerializer'%osm.capitalize()
				Serializer = globals()[serializer_class_name]
				similarities = BaseCartController.similarities(osm, product, osm_name)
				recommendations[osm] = [ Serializer(p, context = {'score': score, 'matching': False}).data for p, score in similarities]

		# Serializing product
		serializer_class_name = '%sRecommendationSerializer'%osm_name.capitalize()
		Serializer = globals()[serializer_class_name]
		serialized = Serializer(product)

		return {'recommendations':recommendations, 'product': serialized.data}

class CartAPIView(BaseAPIView):
	@osm
	def get(self, request, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		cart_controller = request.cart_controller
		serializer_class_name = '%sCartContentSerializer'%osm_name.capitalize()
		Serializer = globals()[serializer_class_name]
		cart_content = getattr(cart_controller.metacart, osm_name+'_cart').cart_content_set.all()
		serialized = Serializer(cart_content, many = True)

		return {'cart':serialized.data}

class CartManagementAPIView(BaseAPIView):
	"""
		Cart Management api view
	"""
	def get_product(self, reference, osm_name):
		
			global_keys = globals().keys()
			product_class_name = '%sProduct'%osm_name.capitalize()

			if product_class_name in global_keys:
				Product = globals()[product_class_name]
				try:
					return Product.objects.get(reference = reference)
				except Product.DoesNotExist:
					raise Http404
			else:
				raise Http404

	@osm
	def post(self, request, reference, quantity = 1, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		product = self.get_product(reference, osm_name)
		cart_controller = request.cart_controller
		if quantity is not None:
			cart_controller.add_product(product, int(quantity))
		else:
			cart_controller.add_product(product)

		carts = { o: {
			'id': cart_controller.carts[o].cart.id,
			'price': cart_controller.carts[o].cart.cart_history_set.all()[0].price,
			'created':cart_controller.carts[o].cart.cart_history_set.all()[0].created,
		}
			for o in cart_controller.carts
		}

		return {'carts':carts}

	@osm
	def delete(self, request, reference, quantity = None, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		product = self.get_product(reference, osm_name)
		cart_controller = request.cart_controller
		if quantity is not None:
			cart_controller.remove_product(product, int(quantity))
		else:
			cart_controller.remove_product(product)

		carts = { o: {
			'id': cart_controller.carts[o].cart.id,
			'price': cart_controller.carts[o].cart.cart_history_set.all()[0].price,
			'created':cart_controller.carts[o].cart.cart_history_set.all()[0].created,
		}
			for o in cart_controller.carts
		}

		return {'carts':carts}




		