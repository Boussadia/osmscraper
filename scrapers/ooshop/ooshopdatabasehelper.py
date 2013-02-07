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

	def get_categories(self, options = {}):
		"""
			Method that retrieves all categories in a hash.

			Input:
				- option (hash) : 
					1. {
						'leaves' : boolean, get categories with no childs (optional),
						'id_parent_category': id of parent category (optional),
						'start_date':  (datetime) retireve category updated after this date (optional),
						'end_date':  (datetime) retireve category updated before this date (optional),
					}

			Output :
				- categories : list of hashs representing categories.
		"""
		categories_entities = Category.objects.all()
		if 'id_parent_category' in options and options['id_parent_category']:
			id_parent_category = options['id_parent_category']
			categories_entities = categories_entities.filter(parent_category_id = id_parent_category)

		if 'start_date' in options and options['start_date']:
			start_date = options['start_date']
			categories_entities = categories_entities.filter(updated__gte=start_date)

		if 'end_date' in options and options['end_date']:
			end_date = options['end_date']
			categories_entities = categories_entities.filter(updated__lte=end_date)

		categories = list(categories_entities)

		if 'leaves' in options and options['leaves']:
			# Keeping only category leaves, i.e. category that are not parent of another category
			# if a parent category is in categories_entities, remove it but get its children
			i = 0
			while i<len(categories):
				category = categories[i]
				sub_categories = Category.objects.filter(parent_category = category)
				if len(sub_categories) == 0:
					# This category is a leaf keep going
					i = i+1
					continue
				else:
					# This is not a leaf, remove it and add sub categories to end of list
					categories.pop(i)
					categories = categories + list(sub_categories)
					continue

		# Organizing categories
		categories = [ {'id': cat.id, 'name': cat.name, 'parent_category_id': cat.parent_category_id, 'url': cat.url} for cat in categories]

		return categories


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


