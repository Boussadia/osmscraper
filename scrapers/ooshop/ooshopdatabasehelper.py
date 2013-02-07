#!/usr/bin/python
# -*- coding: utf-8 -*-

from scrapers.base.basedatabasehelper import BaseDatabaseHelper

from ooshop.models import Category
from ooshop.models import NewBrand
from ooshop.models import NewProduct as Product
from ooshop.models import Promotion
from ooshop.models import History
from ooshop.models import ShippingArea

class OoshopDatabaseHelper(BaseDatabaseHelper):

	def __init__(self):
		super(OoshopDatabaseHelper, self).__init__()

	#-----------------------------------------------------------------------------------------------------------------------
	#
	#									INHERITED METHODS FROM BASE DATABASE HELPER
	#
	#-----------------------------------------------------------------------------------------------------------------------

	def save_categories(self, categories, id_parent_category = None):
		"""
			Method reponsible for saving categories to database.

			Input :
				- categories : list of hash representing categories
				- id_parent_category : if not None, this is the id of the parent category in the database.
			Output :
				- list hash representing saved categories (with id and updated time)
		"""
		saved_categories = []
		# print categories
		for i in xrange(len(categories)):
			category = categories[i]
			name = unicode(category['name'])
			url = unicode(category['url'])
			if id_parent_category:
				category_db, created = Category.objects.get_or_create(url = url, defaults={'name': name, 'parent_category_id': id_parent_category})
			else:
				category_db, created = Category.objects.get_or_create(name = name, defaults={'url': url})

			if not created:
				category_db.name = name
				category_db.parent_category_id = id_parent_category
				category_db.save()

			# Setting id to categories
			category['id'] = category_db.id

			categories[i] = category

		return categories



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
				- id_parent_category : id of parent category
				- start_date (datetime): retireve category updated after this date
				- end_date (datetime): retireve category updated before this date

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
			city_name = shipping_area['city_name']
			postal_code = shipping_area['postal_code']
			is_shipping_area = shipping_area['is_shipping_area']
			area, created = ShippingArea(postal_code = postal_code, defaults={'city_name': city_name, 'is_shipping_area': is_shipping_area})
			if not created:
				area.city_name = city_name
				area.is_shipping_area = is_shipping_area
				area.save()


