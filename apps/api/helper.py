#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from django.db.models import Q, F 

from dalliz.models import Category, Brand
from monoprix.models import History as MonoprixHistory, Product as MonoprixProduct, Promotion as MonoprixPromotion
from ooshop.models import History as OoshopHistory, Product as OoshopProduct, Promotion as OoshopPromotion
from auchan.models import History as AuchanHistory, Product as AuchanProduct, Promotion as AuchanPromotion

from cart.base.basecartcontroller import BaseCartController
from cart.dalliz.dallizcartcontroller import DallizCartController
from cart.models import MetaCart

class ApiHelper(object):
	"""
		This class is created in order to simplify the api view code.
		It only contains static methods.
	"""

	@staticmethod
	def get_products_query_set(category, type_fetched, osm_name = 'monoprix', osm_type='shipping', osm_location=None, brands = []):
		"""
			Returns query set corresponding to query filters
		"""
		global_keys = globals().keys()
		products_query_set = None

		# Building QuerySet
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
				products_query_set = Product.objects.filter(~Q(promotion__end__lte = F('history__created'))).filter(**kwargs).distinct('reference')
			else:
				kwargs.update({'dalliz_category': category})
				products_query_set = Product.objects.filter(**kwargs).distinct('reference')

			# Filtering before slicing
			# Filtering by brands
			if len(brands)>0:
				products_query_set = products_query_set.filter(brand__brandmatch__dalliz_brand__id__in = brands)

		return products_query_set

