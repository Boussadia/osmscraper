#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from datetime import datetime, timedelta

from django.db.models import Q, F 
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404

from rest_framework import status, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.renderers import XMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from scrapers.ooshop.ooshopscraper import OoshopScraper

from cart.base.basecartcontroller import BaseCartController
from cart.dalliz.dallizcartcontroller import DallizCartController
from cart.models import MetaCart

from auchan.models import History as AuchanHistory, Product as AuchanProduct, Promotion as AuchanPromotion

from dalliz.models import Category

from monoprix.models import History as MonoprixHistory, Product as MonoprixProduct, Promotion as MonoprixPromotion

from ooshop.models import History as OoshopHistory, Product as OoshopProduct, Promotion as OoshopPromotion

from api.renderer import ProductsCSVRenderer, ProductRecommendationCSVRenderer, NewProductsCSVRenderer
from api.serializer.dalliz.serializer import CategorySerializer, UserSerializer, BrandSerializer
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

		# Getting session/user information for metacart retrieval
		session_key = request.session.session_key
		user = request.user

		# Getting metacart
		metacart = None

		if user.is_anonymous() and session_key is not None:
			# If not logged in, get metacart by session id
			metacart = MetaCart.objects.filter(session__session_key = session_key)
			if len(metacart)>0:
				# Metacart retrieved
				metacart = metacart[0]
			else:
				# No metacart set for this session, create one and associate it to session
				metacart = MetaCart(session = Session.objects.get(session_key = session_key))
				metacart.save()
		elif not user.is_anonymous():
			# User is authenticated, retrieve metacart
			metacart = MetaCart.objects.get(user = user)

		# Setting cart
		cart_controller = DallizCartController(osm = metacart.current_osm, metacart = metacart)
		request.cart_controller = cart_controller

		# Default osm
		osm = {
			'name':metacart.current_osm,
			'type':'shipping',
			'location':None,
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

		if not isinstance(data, Response):
			return Response(data)

		return data
	return wrapper

class BaseAPIView(APIView):
	"""
			Base Api view for dalliz api.
	"""
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [XMLRenderer]
	authentication_classes = (SessionAuthentication, )

class BetaRestrictionAPIView(APIView):
	"""
		Restricting access to beta users only.
	"""
	permission_classes = (permissions.IsAuthenticated, )


#----------------------------------------------------------------------------------------------------------------------------------------------
#
#														USER
#
#----------------------------------------------------------------------------------------------------------------------------------------------


class UserAPI(BaseAPIView):
	"""
		User api view.
	"""

	def get(self, request):
		try:
			data = UserSerializer(request.user).data
			return Response(data)
		except Exception, e:
			return Response({})


	def post(self, request):
		if 'username' in request.POST and 'password' in request.POST:
			# login user
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)

			if user is not None:
				login(request, user)
				data = UserSerializer(user).data

				# Now checking if user is associated with meta cart
				metacart = MetaCart.objects.filter(user = user)
				if metacart.count()>0:
					# Metacart retrieved, ok nothing to do
					pass
				else:
					# No metacart set for this user, check if the current session is associated with metacart
					metacart = MetaCart.objects.filter(session = request.session)
					if metacart.count()>0:
						# Metacart retrieved, associate it with user
						metacart = metacart[0]
						metacart.user = user
						metacart.save()
					else:
						# No cart was found, create one and associate it with user
						metacart = MetaCart(user = user)
						metacart.save()
			else:
				raise AuthenticationFailed

			return Response(data)
		else:
			# logout user
			logout(request)
			return Response({})



#----------------------------------------------------------------------------------------------------------------------------------------------
#
#														CATEGORIES
#
#----------------------------------------------------------------------------------------------------------------------------------------------

class CategoryAll(BetaRestrictionAPIView):
	"""
		View for all category.
	"""
	@osm
	def get(self, request, format=None,**kwargs):
		data = CategorySerializer.all()
		return data


class CategorySimple(BetaRestrictionAPIView):
	"""
		Get single category view.
	"""
	def get_object(self, id_category):
		try:
			return Category.objects.get(id=id_category)
		except Category.DoesNotExist:
			raise Http404
	@osm
	def get(self, request, id_category, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		category = self.get_object(id_category)
		subs = CategorySerializer.all(category, leaves=True, osm_name = osm_name, osm_type = osm_type, osm_location = osm_location)
		data = CategorySerializer(category).data
		data.update({'subs': subs})
		if data is None:
			return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
		else:
			return data

class CategoryProducts(CategorySimple):
	"""
		Get products for a category
	"""
	TOP_PRODUCTS_COUNT = 5
	MID_PRODUCTS_COUNT = 17
	renderer_classes = BetaRestrictionAPIView.renderer_classes + [ProductsCSVRenderer]
	@osm
	def get(self, request, id_category, type_fetched, key, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		category = self.get_object(id_category)
		serialized = None
		global_keys = globals().keys()

		# Settings location kwargs :
		kwargs_location_history = {}
		kwargs_location_promotion = {}
		if osm_name == 'monoprix':
			if osm_location is None:
				kwargs_location_history['history__store__isnull'] = True
				kwargs_location_promotion['promotion__store__isnull'] = True
			else:
				kwargs_location_history['history__store__id'] = osm_location
				kwargs_location_promotion['promotion__store__id'] = osm_location
		else:
			if osm_location is None:
				kwargs_location_history['history__shipping_area__isnull'] = True
				kwargs_location_promotion['promotion__shipping_area__isnull'] = True
			else:
				kwargs_location_history['history__shipping_area__id'] = osm_location
				kwargs_location_promotion['promotion__shipping_area__id'] = osm_location

		# Getting products without simple promotion
		product_class_name = '%sProduct'%osm_name.capitalize()
		if product_class_name in global_keys:
			Product = globals()[product_class_name]
			kwargs = {
				'exists':True,
			}
			kwargs.update(kwargs_location_history) # adding location filter
			kwargs.update(kwargs_location_promotion)

			if type_fetched == 'promotions':
				kwargs.update({'promotion__id__isnull': False, 'promotion__type' : 's','dalliz_category__parent_category': category}) # Only handeling simple promotions
				products = Product.objects.filter(~Q(promotion__end__lte = F('history__created'))).filter(**kwargs).distinct('reference')
			else:
				kwargs.update({'dalliz_category': category})
				products = Product.objects.filter(**kwargs).distinct('reference')

			products_count = products.count() # Adding total count of products in category

			# Now getting brands information
			brands = set([ p.brand.brandmatch_set.all()[0].dalliz_brand for p in products[:] if p.brand is not None and p.brand.brandmatch_set.all().count()==1])
			brands_count = len(brands)

			if 'TOP_PRODUCTS_COUNT' in request.GET:
				CategoryProducts.TOP_PRODUCTS_COUNT = request.GET['TOP_PRODUCTS_COUNT']

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
			serialized = Serializer_class(products, many = True, context = {'osm': {'name':osm_name,'type': osm_type, 'location':osm_location}, 'time':datetime.now(), 'cart': cart, 'type': type_fetched})
		if serialized is None:
			return Response(404, status=status.HTTP_400_BAD_REQUEST)
		else:
			response = serialized.data
			return response

class CategoryMatching(CategorySimple):
	"""
		Get recommendation for product
	"""
	renderer_classes = BetaRestrictionAPIView.renderer_classes + [ProductRecommendationCSVRenderer]

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
			return serialized


#----------------------------------------------------------------------------------------------------------------------------------------------
#
#														PRODUCTS
#
#----------------------------------------------------------------------------------------------------------------------------------------------


class NewProducts(BetaRestrictionAPIView):
	"""
		API view for extracting new products (created in the last 7 days)
	"""
	renderer_classes = BetaRestrictionAPIView.renderer_classes + [NewProductsCSVRenderer]

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
			return serialized

class Product(BetaRestrictionAPIView):
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
			serialized = Serializer(product, context = {'osm': {'name':osm['name'],'type': osm_type, 'location':osm_location}})

		if serialized is None:
			return Response(404, status=status.HTTP_400_BAD_REQUEST)
		else:
			return serialized.data

class ProductRecommendation(Product):
	"""
		Get Recommendation for product
	"""
	# renderer_classes = BetaRestrictionAPIView.renderer_classes + [ProductRecommendationCSVRenderer]

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
					recommendations[osm['name']] = [ Serializer(match, context = {'osm': {'name':osm_name,'type': osm_type, 'location':osm_location}, 'matching': True}).data]
					osm_recommendation.remove(osm['name'])

		# Processing recommendation
		for osm in osm_recommendation:
			if osm != osm_name:
				serializer_class_name = '%sRecommendationSerializer'%osm.capitalize()
				Serializer = globals()[serializer_class_name]
				similarities = BaseCartController.similarities(osm, product, osm_name)
				recommendations[osm] = [ Serializer(p, context = {'osm': {'name':osm_name,'type': osm_type, 'location':osm_location}, 'score': score, 'matching': False}).data for p, score in similarities]
		return {'recommendations':recommendations}


#----------------------------------------------------------------------------------------------------------------------------------------------
#
#														CART
#
#----------------------------------------------------------------------------------------------------------------------------------------------

class CartAPIView(BetaRestrictionAPIView):
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
	def get(self, request, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		# Getting cart for osm
		cart_controller = request.cart_controller
		cart = getattr(cart_controller.metacart, osm_name+'_cart')

		# Getting all main categories
		main_categories = Category.objects.filter(parent_category = None)
		data = []

		serializer_class_name = '%sCartContentSerializer'%osm_name.capitalize()
		Serializer = globals()[serializer_class_name]

		quantity_products = 0

		for category in main_categories:
			# Filtering by main category
			category_cart = {'name': category.name}
			cart_content = cart.cart_content_set.filter(product__dalliz_category__parent_category__parent_category = category).distinct('product')

			# Serializing products
			serialized = Serializer(cart_content, many = True, context = {'osm': {'name':osm_name,'type': osm_type, 'location':osm_location}, 'time':datetime.now(), 'cart': cart})
			category_cart['products'] = serialized.data


			if len(serialized.data)>0:
				category_cart['products'] = serialized.data
				# Computing total price
				category_cart['price'] = sum([ product['product']['history'][0]['price']*product['quantity'] for product in category_cart['products']])
				for osm in AVAILABLE_OSMS:
					try:
						if osm['name'] != osm_name:
							category_cart[osm['name']+'_price'] = sum([ product[osm['name']+'_product']['history'][0]['price']*product['>
						else:
							category_cart[osm['name']+'_price'] = category_cart['price']
						except Exception,e:
							category_cart[osm['name'] = 0


				quantity_products = quantity_products + sum([ product['quantity'] for product in category_cart['products']])
				data.append(category_cart)


		return {'content': data, 'name': osm_name, 'quantity': quantity_products}

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
			'active': (request.cart_controller.metacart.current_osm == cart_controller.carts[o].cart.osm)
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
			'active': (request.cart_controller.metacart.current_osm == cart_controller.carts[o].cart.osm)
		}
			for o in cart_controller.carts
		}

		return {'carts':carts}

class CartImportation(BetaRestrictionAPIView):
	"""
		Import cart from ooshop.
	"""

	@osm
	def post(self, request, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		ooshop_email = request.DATA['email']
		ooshop_password = request.DATA['password']

		# Getting cart content from ooshop site
		scraper = OoshopScraper()
		cart, code, is_logued = scraper.import_cart(user_email = ooshop_email, password = ooshop_password)
		
		if not is_logued:
			raise AuthenticationFailed
		else:
			# Setting cart 
			cart_controller = request.cart_controller
			cart_controller.set_osm('ooshop')
			cart_controller.empty()
			for content in cart:
				product = OoshopProduct.objects.filter(reference = content['reference'])
				if product.count() == 0:
					print 'Product not found : '+content['reference']
				else:
					product = product[0]
					cart_controller.add_product(product, content['quantity'])

			return {'test': cart}


#----------------------------------------------------------------------------------------------------------------------------------------------
#
#														OSM
#
#----------------------------------------------------------------------------------------------------------------------------------------------

class OSMSAPIView(BetaRestrictionAPIView):
	"""
		This class handles osm switching.
	"""

	def get_osms(self, cart_controller):
		osms = []
		# No computing necessary
		active_osm = {
			'name':cart_controller.metacart.current_osm,
			'type':'shipping',
			'location':None,
			'active': True,
			'price': cart_controller.carts[cart_controller.metacart.current_osm].price

		}

		osms.append(active_osm)
		
		for o in AVAILABLE_OSMS:
			if o['name'] != active_osm['name']:
				osms.append({
					'name':o['name'],
					'type':'shipping',
					'location':None,
					'active': False,
					'price': cart_controller.carts[o['name']].price
				})

		return osms


	@osm
	def get(self, request, **kwargs):

		return self.get_osms(request.cart_controller)

	@osm
	def post(self, request, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		new_osm_name = request.DATA['new_name']
		if 'new_type' in request.DATA:
			new_osm_type = request.DATA['new_type']
		if 'new_location' in request.DATA:
			new_osm_location = request.DATA['new_location']
		request.cart_controller.set_osm(new_osm_name)
		osm = {
			'name':request.cart_controller.metacart.current_osm,
			'type':'shipping',
			'location':None,
			'active': True,
			'price': request.cart_controller.carts[request.cart_controller.metacart.current_osm].price

		}
		return osm




		