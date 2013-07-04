#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from datetime import datetime, timedelta

from django.db.models import Q, F 
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404

from rest_framework import status, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed, APIException
from rest_framework.renderers import XMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from apps.scrapers.ooshop.ooshopscraper import OoshopScraper
from apps.scrapers.monoprix.monoprixscraper import MonoprixScraper
from apps.scrapers.auchan.auchanscraper import AuchanScraper

from dalliz.models import Category

from monoprix.models import History as MonoprixHistory, Product as MonoprixProduct, Promotion as MonoprixPromotion
from ooshop.models import History as OoshopHistory, Product as OoshopProduct, Promotion as OoshopPromotion
from auchan.models import History as AuchanHistory, Product as AuchanProduct, Promotion as AuchanPromotion

from cart.base.basecartcontroller import BaseCartController
from cart.dalliz.dallizcartcontroller import DallizCartController
from cart.models import MetaCart

from apps.api.helper import ApiHelper
from apps.api.renderer import ProductsCSVRenderer, ProductRecommendationCSVRenderer, NewProductsCSVRenderer
from apps.api.serializer.dalliz.serializer import CategorySerializer, UserSerializer, BrandSerializer
from apps.api.serializer.auchan.serializer import ProductSerializer as AuchanProductSerializer, ProductsPaginationSerializer as AuchanProductsPaginationSerializer, CartContentSerializer as AuchanCartContentSerializer
from apps.api.serializer.auchan.serializer import RecommendationSerializer as AuchanRecommendationSerializer
from apps.api.serializer.monoprix.serializer import ProductSerializer as MonoprixProductSerializer, ProductsPaginationSerializer as MonoprixProductsPaginationSerializer, CartContentSerializer as MonoprixCartContentSerializer
from apps.api.serializer.monoprix.serializer import RecommendationSerializer as MonoprixRecommendationSerializer
from apps.api.serializer.ooshop.serializer import ProductSerializer as OoshopProductSerializer, ProductsPaginationSerializer as OoshopProductsPaginationSerializer
from apps.api.serializer.ooshop.serializer import RecommendationSerializer as OoshopRecommendationSerializer, CartContentSerializer as OoshopCartContentSerializer

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

class OSMNotFoundException(APIException):
	status_code = 500
	detail = 'OSM not found'


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
	PRODUCTS_PER_PAGE = 5
	PAGE = 1
	renderer_classes = BetaRestrictionAPIView.renderer_classes + [ProductsCSVRenderer]

	@osm
	def get(self, request, id_category, type_fetched, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		category = self.get_object(id_category)
		global_keys = globals().keys()
		serialized = None

		# Brands filter parameter
		brands = request.QUERY_PARAMS.getlist('brands[]')

		# Pagination arguments
		if 'PRODUCTS_PER_PAGE' in request.GET:
			CategoryProducts.PRODUCTS_PER_PAGE = request.QUERY_PARAMS.get('PRODUCTS_PER_PAGE')

		if 'page' in request.GET:
			page = request.QUERY_PARAMS.get('page')
		else:
			page = CategoryProducts.PAGE

		# Getting query from api helper class
		products_query_set = ApiHelper.get_products_query_set(category, type_fetched, osm_name, osm_type, osm_location, brands)

		if products_query_set is not None:
			# Generating pagination object
			paginator = Paginator(products_query_set, CategoryProducts.PRODUCTS_PER_PAGE)
			try:
				products = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				products = paginator.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999),
				# deliver last page of results.
				products = paginator.page(paginator.num_pages)


		serializer_class_name = '%sProductsPaginationSerializer'%osm_name.capitalize()
		serializer = None

		if serializer_class_name in global_keys:
			cart = getattr(request.cart_controller.metacart, osm_name+'_cart')
			context = {'osm': {'name':osm_name,'type': osm_type, 'location':osm_location}, 'time':datetime.now(), 'cart': cart, 'type': type_fetched}
			Serializer_class = globals()[serializer_class_name]
			serializer = Serializer_class(products, context = context)
		if serializer is None:
			return Response(404, status=status.HTTP_400_BAD_REQUEST)
		else:
			response = serializer.data
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

	def get_content(self, content_id, cart_controller, osm_name):
		try:
			cart = getattr(cart_controller.metacart, '%s_cart'%(osm_name))
			return cart.cart_content_set.get(id = content_id)
		except Exception, e:
			return None


	@osm
	def get(self, request, reference, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		product = self.get_product(reference, osm_name)
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

	@osm
	def get(self, request, reference, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		product = self.get_product(reference, osm_name)
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

	@osm
	def post(self, request, reference, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		if 'content_id' in request.DATA and 'reference_selected' in request.DATA and 'osm_selected' in request.DATA:
			content_id = request.DATA['content_id']
			product_reference_selected = request.DATA['reference_selected']
			osm_selected = request.DATA['osm_selected']
			cart_controller = request.cart_controller

			product = self.get_product(product_reference_selected, osm_selected)
			cart_content = self.get_content(content_id, cart_controller, osm_selected)
			cart_content.product = product
			cart_content.is_user_added = False
			cart_content.is_match = False
			cart_content.is_suggested = True
			cart_content.is_user_set = True
			cart_content.save()

			return {'ok':True}

		else:
			return {'ok':False}


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

	def get_content(self, content_id, cart_controller, osm_name):
		try:
			cart = getattr(cart_controller.metacart, '%s_cart'%(osm_name))
			return cart.cart_content_set.get(id = content_id)
		except Exception, e:
			return None

	def get_serialized_product(self, product, osm_name = 'monoprix', osm_type='shipping', osm_location=None, cart_controller = None):
		if cart_controller:
			cart = getattr(cart_controller.metacart, osm_name+'_cart')
		else:
			cart = None

		global_keys = globals().keys()
		serialized = None
		serializer_class_name = '%sProductSerializer'%osm_name.capitalize()
		if serializer_class_name in global_keys:
			Serializer = globals()[serializer_class_name]
			serialized = Serializer(product, context = {'osm': {'name':osm_name,'type': osm_type, 'location':osm_location}})


		if serialized is None:
			return Response(404, status=status.HTTP_400_BAD_REQUEST)
		else:
			data = serialized.data
			quantity = 0
			content_id = None
			if cart:
				for content in cart.cart_content_set.filter(product = product):
					if content.product == product:
						quantity = quantity + content.quantity
						content_id = content.id
			data['quantity_in_cart'] = quantity
			data['content_id'] = content_id
			return data

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
			cart_content = cart.cart_content_set.filter(product__dalliz_category__parent_category__parent_category = category).distinct('id')

			# Serializing products
			serialized = Serializer(cart_content, many = True, context = {'osm': {'name':osm_name,'type': osm_type, 'location':osm_location}, 'time':datetime.now(), 'cart': cart})
			category_cart['products'] = serialized.data


			if len(serialized.data)>0:
				category_cart['products'] = serialized.data
				# Computing total price
				category_cart['price'] = sum([ product['product']['history'][0]['price']*product['quantity'] for product in category_cart['products'] if len(product['product']['history'])>0 ])
				for osm in AVAILABLE_OSMS:
					try:
						if osm['name'] != osm_name:
							category_cart[osm['name']+'_price'] = sum([ product[osm['name']+'_product']['history'][0]['price']*product['quantity'] for product in category_cart['products'] if product[osm['name']+'_product'] is not None])
						else:
							category_cart[osm['name']+'_price'] = category_cart['price']
					except Exception, e:
						category_cart[osm['name']+'_price'] = 0


				quantity_products = quantity_products + sum([ product['quantity'] for product in category_cart['products']])
				data.append(category_cart)


		return {'content': data, 'name': osm_name, 'quantity': quantity_products, 'id': cart_controller.metacart.id}

	@osm
	def post(self, request, reference, quantity = 1, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		content_id = None
		if 'content_id' in request.DATA:
			content_id = request.DATA['content_id']

		cart_controller = request.cart_controller

		if content_id is None:
			# This is a new product in cart
			product = self.get_product(reference, osm_name)

			if quantity is not None:
				cart_controller.add_product(product, int(quantity))
			else:
				cart_controller.add_product(product)
		else:
			# This is a product that is already in the cart
			content = self.get_content(content_id, cart_controller, osm_name)

			if content is not None:
				if quantity is not None:
					cart_controller.add(content, int(quantity))
				else:
					cart_controller.add(content)

				# Getting product for response
				product = content.product
			else:
				product = self.get_product(reference, osm_name)


		return self.get_serialized_product(product, osm_name, osm_type, osm_location, cart_controller)

	@osm
	def delete(self, request, reference = None, quantity = None, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		content_id = None
		if 'content_id' in request.DATA:
			content_id = request.DATA['content_id']

		cart_controller = request.cart_controller
		if content_id:
			# removing  from cart
			content = self.get_content(content_id, cart_controller, osm_name)
			if quantity is not None:
				cart_controller.remove(content, int(quantity))
			else:
				cart_controller.remove(content)

			return self.get_serialized_product(content.product, osm_name, osm_type, osm_location, cart_controller)

		else:
			# Emptying the whole cart
			cart_controller.empty()
			return {'content': [], 'name': osm_name, 'quantity': 0, 'id': cart_controller.metacart.id}

class CartImportation(BetaRestrictionAPIView):
	"""
		Import cart from osm.
	"""

	@osm
	def post(self, request, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		email = request.DATA['email']
		password = request.DATA['password']


		global_keys = globals().keys()

		# Getting cart content from osm site
		scraper_class_name = '%sScraper'%(osm_name.capitalize())
		product_class_name = '%sProduct'%(osm_name.capitalize())
		if scraper_class_name in global_keys:
			Scraper = globals()[scraper_class_name]
			Product = globals()[product_class_name]
			scraper = Scraper()
			cart, code, is_logued = scraper.import_cart(user_email = email, password = password)
			
			if not is_logued:
				return {'error': {
					'status': 403,
					'msg': 'Credentials not valid'
				}}
			else:
				# Setting cart 
				cart_controller = request.cart_controller
				cart_controller.set_osm(osm_name)
				cart_controller.empty()
				for content in cart:
					product = Product.objects.filter(reference = content['reference'])
					if product.count() == 0:
						print 'Product not found : '+content['reference']
					else:
						product = product[0]
						cart_controller.add_product(product, content['quantity'])

				return {'cart': cart}
		else:
			raise OSMNotFoundException


class CartExport(BetaRestrictionAPIView):
	"""
		Import cart from ooshop.
	"""

	@osm
	def post(self, request, osm_name = 'ooshop', osm_type='shipping', osm_location=None):
		cart_controller = request.cart_controller

		email = request.DATA['email']
		password = request.DATA['password']
		global_keys = globals().keys()

		# Getting cart content from osm site
		scraper_class_name = '%sScraper'%(osm_name.capitalize())
		if scraper_class_name in global_keys:
			Scraper = globals()[scraper_class_name]
			scraper = Scraper()
			products = cart_controller.get_products_for_export(osm_name)
			feedback = scraper.export_cart(products, user_email = email, password = password)
			return feedback
		else:
			raise OSMNotFoundException


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




		