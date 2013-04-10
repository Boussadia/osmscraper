#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from datetime import datetime, timedelta

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.settings import api_settings
from rest_framework.renderers import XMLRenderer

from auchan.models import History as AuchanHistory, Product as AuchanProduct, Promotion as AuchanPromotion
from dalliz.models import Category
from monoprix.models import History as MonoprixHistory, Product as MonoprixProduct, Promotion as MonoprixPromotion
from ooshop.models import History as OoshopHistory, Product as OoshopProduct, Promotion as OoshopPromotion

from api.renderer import ProductsCSVRenderer, ProductRecommendationCSVRenderer, NewProductsCSVRenderer
from api.serializer.dalliz.serializer import CategorySerializer
from api.serializer.auchan.serializer import ProductSerializer as AuchanProductSerializer
from api.serializer.auchan.serializer import RecommendationSerializer as AuchanRecommendationSerializer
from api.serializer.monoprix.serializer import ProductSerializer as MonoprixProductSerializer
from api.serializer.monoprix.serializer import RecommendationSerializer as MonoprixRecommendationSerializer
from api.serializer.ooshop.serializer import ProductSerializer as OoshopProductSerializer
from api.serializer.ooshop.serializer import RecommendationSerializer as OoshopRecommendationSerializer

from cart.base.basecartcontroller import BaseCartController

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

		kwargs.update(dict([ ( 'osm_%s'%k , v) for k,v in osm.iteritems()]))

		data = function( self , *args, **kwargs)

		if isinstance(data, dict):
			data.update({'osm': osm})
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
	TOP_PRODUCTS_COUNT = 10
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

		# # Getting promotions
		# promotion_class_name = '%sPromotion'%osm_name.capitalize()
		# if promotion_class_name in global_keys:
		# 	Promotion = globals()[promotion_class_name]
		# 	kwargs = {
		# 		'end__gte': datetime.now(),
		# 		'content__dalliz_category': category,
		# 	}
		# 	kwargs.update(kwargs_location_promotion) # adding location filter
		# 	promotions = Promotion.objects.filter(**kwargs)
		# 	print promotions[0].type == Promotion.SIMPLE

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
			if key == 'top':
				products = products[:CategoryProducts.TOP_PRODUCTS_COUNT]

		serializer_class_name = '%sProductSerializer'%osm_name.capitalize()
		
		if serializer_class_name in global_keys:
			Serializer_class = globals()[serializer_class_name]
			serialized = Serializer_class(products, many = True, context = {'osm': {'name':osm_name,'type': osm_type, 'location':osm_location}, 'time':datetime.now()})
		if serialized is None:
			return Response(404, status=status.HTTP_400_BAD_REQUEST)
		else:
			return {'products':serialized.data}

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



		