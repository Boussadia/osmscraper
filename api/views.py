#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from rest_framework.settings import api_settings
from rest_framework.renderers import XMLRenderer
from api.renderer import ProductsCSVRenderer, ProductRecomandationCSVRenderer

from ooshop.models import History as OoshopHistory, Product as OoshopProduct
from monoprix.models import History as MonoprixHistory, Product as MonoprixProduct
from auchan.models import History as AuchanHistory, Product as AuchanProduct

from api.serializer.dalliz.serializer import CategorySerializer
from api.serializer.auchan.serializer import ProductSerializer as AuchanProductSerializer
from api.serializer.auchan.serializer import HistorySerializer as AuchanHistorySerializer
from api.serializer.auchan.serializer import RecomandationSerializer as AuchanRecomandationSerializer
from api.serializer.monoprix.serializer import ProductSerializer as MonoprixProductSerializer
from api.serializer.monoprix.serializer import HistorySerializer as MonoprixHistorySerializer
from api.serializer.monoprix.serializer import RecomandationSerializer as MonoprixRecomandationSerializer
from api.serializer.ooshop.serializer import ProductSerializer as OoshopProductSerializer
from api.serializer.ooshop.serializer import HistorySerializer as OoshopHistorySerializer
from api.serializer.ooshop.serializer import RecomandationSerializer as OoshopRecomandationSerializer

from cart.base.basecartcontroller import BaseCartController

from dalliz.models import Category

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

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
		# category = self.get_object(id_category)
		# serialized = None
		# global_keys = globals().keys()
		# history_class_name = '%sHistory'%osm_name.capitalize()
		# if history_class_name in global_keys:
		# 	History = globals()[history_class_name]
		# 	kwargs = {
		# 		'product__exists':True,
		# 		'product__dalliz_category': category
		# 	}

		# 	if osm_name == 'monoprix':
		# 		if osm_location is None:
		# 			kwargs['store__isnull'] = True
		# 		else:
		# 			kwargs['store__id'] = osm_location
		# 	else:
		# 		if osm_location is None:
		# 			kwargs['shipping_area__isnull'] = True
		# 		else:
		# 			kwargs['shipping_area__id'] = osm_location

		# 	histories = History.objects.filter(**kwargs).distinct('product')
		# 	if key == 'top':
		# 		histories = histories[:CategoryProducts.TOP_PRODUCTS_COUNT]

		# serializer_class_name = '%sHistorySerializer'%osm_name.capitalize()
		
		# if serializer_class_name in global_keys:
		# 	Serializer_class = globals()[serializer_class_name]
		# 	serialized = Serializer_class(histories, many = True)
		# if serialized is None:
		# 	return Response(404, status=status.HTTP_400_BAD_REQUEST)
		# else:
		# 	return {'products':serialized.data}
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
			if key == 'top':
				products = products[:CategoryProducts.TOP_PRODUCTS_COUNT]

		serializer_class_name = '%sProductSerializer'%osm_name.capitalize()
		
		if serializer_class_name in global_keys:
			Serializer_class = globals()[serializer_class_name]
			serialized = Serializer_class(products, many = True, context = {'osm': {'name':osm_name,'type': osm_type, 'location':osm_location}})
		if serialized is None:
			return Response(404, status=status.HTTP_400_BAD_REQUEST)
		else:
			return {'products':serialized.data}

class CategoryMatching(CategorySimple):
	"""
		Get recomandation for product
	"""
	# renderer_classes = BaseAPIView.renderer_classes + [ProductRecomandationCSVRenderer]

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
				print matching
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

class ProductRecomandation(Product):
	"""
		Get recomandation for product
	"""
	# renderer_classes = BaseAPIView.renderer_classes + [ProductRecomandationCSVRenderer]

	@osm
	def get(self, request, reference, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		product = self.get_object(reference, osm_name)
		global_keys = globals().keys()
		serialized = None
		recomandations = {}
		osm_recomandation = [ osm['name'] for osm in AVAILABLE_OSMS if osm['name'] != osm_name]
		# print osm_recomandation
		# Processing matching
		matching = product.productmatch_set.all()
		if len(matching)>0:
			matching = matching[0]
			for osm in AVAILABLE_OSMS:
				match = getattr(matching, '%s_product'%osm['name'])
				if match is not None and osm['name'] != osm_name and osm['name'] in osm_recomandation:
					serializer_class_name = '%sRecomandationSerializer'%osm['name'].capitalize()
					Serializer = globals()[serializer_class_name]
					recomandations[osm['name']] = [ Serializer(match, context = { 'matching': True}).data]
					osm_recomandation.remove(osm['name'])

		for osm in osm_recomandation:
			if osm != osm_name:
				serializer_class_name = '%sRecomandationSerializer'%osm.capitalize()
				Serializer = globals()[serializer_class_name]
				recomandations[osm] = [ Serializer(p, context = {'score': score, 'matching': False}).data for p, score in BaseCartController.similarities('auchan', product, osm_name)]

		# Serializing product
		serializer_class_name = '%sRecomandationSerializer'%osm_name.capitalize()
		Serializer = globals()[serializer_class_name]
		serialized = Serializer(product)

		return {'recomandations':recomandations, 'product': serialized.data}



		