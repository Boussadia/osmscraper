#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from ooshop.models import History as OoshopHistory
from monoprix.models import History as MonoprixHistory
from auchan.models import History as AuchanHistory

from serializer.dalliz.serializer import CategorySerializer
from serializer.auchan.serializer import ProductSimpleSerializer as AuchanProductSimpleSerializer, HistorySerializer as AuchanHistorySerializer
from serializer.monoprix.serializer import ProductSimpleSerializer as MonoprixProductSimpleSerializer, HistorySerializer as MonoprixHistorySerializer
from serializer.ooshop.serializer import ProductSimpleSerializer as OoshopProductSimpleSerializer, HistorySerializer as OoshopHistorySerializer

from dalliz.models import Category

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
	def wrapper( self ,request,  *args, **kwargs):
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

		data = function( self ,request, *args, **kwargs)

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
    pass

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
		Get top products for a category
	"""
	TOP_PRODUCTS_COUNT = 10
	@osm
	def get(self, request, id_category, key, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		category = self.get_object(id_category)
		serialized = None
		global_keys = globals().keys()
		history_class_name = '%sHistory'%osm_name.capitalize()
		if history_class_name in global_keys:
			History = globals()[history_class_name]
			kwargs = {
				'product__exists':True,
				'product__dalliz_category': category
			}

			if osm_name == 'monoprix':
				if osm_location is None:
					kwargs['store__isnull'] = True
				else:
					kwargs['store__id'] = osm_location
			else:
				if osm_location is None:
					kwargs['shipping_area__isnull'] = True
				else:
					kwargs['shipping_area__id'] = osm_location

			histories = History.objects.filter(**kwargs).distinct('product')
			if key == 'top':
				histories = histories[:CategoryProducts.TOP_PRODUCTS_COUNT]

		serializer_class_name = '%sHistorySerializer'%osm_name.capitalize()
		
		if serializer_class_name in global_keys:
			Serializer_class = globals()[serializer_class_name]
			serialized = Serializer_class(histories, many = True)
		if serialized is None:
			return Response(404, status=status.HTTP_400_BAD_REQUEST)
		else:
			return {'products':serialized.data}



