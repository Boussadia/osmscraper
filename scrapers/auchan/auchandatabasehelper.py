#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date

from django.db import connection
from django.db import DatabaseError

from scrapers.base.basedatabasehelper import BaseDatabaseHelper

from auchan.models import Category
# from auchan.models import Brand
# from auchan.models import Unit
# from auchan.models import Product
# from auchan.models import Promotion
# from auchan.models import History
from auchan.models import ShippingArea

class AuchanDatabaseHelper(BaseDatabaseHelper):

	def __init__(self):
		super(AuchanDatabaseHelper, self).__init__()

	#-----------------------------------------------------------------------------------------------------------------------
	#
	#									INHERITED METHODS FROM BASE DATABASE HELPER
	#
	#-----------------------------------------------------------------------------------------------------------------------

	def save_categories(self, categories):
		"""
			Method reponsible for saving categories to database.

			Input :
				- categories : list of hash representing categories
		"""

		for main_category in categories:
			main_category_db, created = Category.objects.get_or_create(name = main_category['name'])

			for category_level_1 in main_category['sub_categories']:
				category_level_1_db, created = Category.objects.get_or_create(name = category_level_1['name'], defaults = {'url': category_level_1['url'], 'parent_category': main_category_db})

				if not created:
					category_level_1_db.url = category_level_1['url']
					category_level_1_db.parent_category = main_category_db

				for category_level_2 in category_level_1['sub_categories']:
					category_level_2_db, created = Category.objects.get_or_create(name = category_level_2['name'], defaults = {'url': category_level_2['url'], 'parent_category': category_level_1_db})

					if not created:
						category_level_2_db.url = category_level_2['url']
						category_level_2_db.parent_category = category_level_1_db
		

	def save_products(self, products, id_parent_category):
		"""
			Method responsible for saving products to database
		"""
		pass

	def get_products(self, options = {}):
		"""
			Method responsible for retireving products from database.

			Input :
				- option (hash) : 
					1. {
						'type': 'single',
						'filter':{
							'reference': '...' (optional)
							'image_url': '...',(optional, if reference is not set),
						}
					}
					2. {
						'type': 'multi',
						'filter': {
							'after_date': 'datetime' (optional retrieve products updated after date),
							'before_date': 'datetime' (optional retrieve products older than date),
							'category_id': id (optional)
						}
					}
			Output : 
				- list of products (represented by hash)
		"""
		pass

	def get_categories(self, id_parent_category = None, start_date = None, end_date = None):
		"""
			Method that retrieves all categories in a hash.

			Input:
				- option (hash) : 
					1. {
						'leaves' : boolean, get categories with no childs (optional, but if present all the other options are ignored)
						'id_parent_category': id of parent category (optional),
						'start_date':  (datetime) retireve category updated after this date (optional),
						'end_date':  (datetime) retireve category updated before this date (optional),
					}

			Output :
				- categories : list of hashs representing categories.

			Output :
				- categories : list of hashs representing categories.
		"""
		pass

	def get_shipping_areas(self):
		"""
			Method reponsible for retrieving shipping areas

			Output :
				- list of hash : {'id':..., 'city_name': ..., 'postal_code': .....}
		"""
		pass

	def save_shipping_areas(self, shipping_areas):
		"""
			Method that handle shipping areas saving

			Input :
				- shipping_area (list of hash) : {'city_name': ..., 'postal_code': ....., 'is_shipping_area': Bool}
		"""

		for shipping_area in shipping_areas:
			city_name = shipping_area['name']
			postal_code = shipping_area['postal_code']
			is_shipping_area = shipping_area['is_shipping_area']
			area, created = ShippingArea.objects.get_or_create(postal_code = postal_code,city_name = city_name, defaults={ 'is_shipping_area': is_shipping_area})
			if not created:
				area.city_name = city_name
				area.is_shipping_area = is_shipping_area
				area.save()