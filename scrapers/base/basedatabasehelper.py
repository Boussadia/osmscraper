#!/usr/bin/python
# -*- coding: utf-8 -*-

import simplejson as json
from django.core import serializers

class BaseDatabaseHelper(object):
	"""
		This class si responsible for interfacing with the database.
	"""

	def __init__(self):
		pass

	def save_categories(self, categories, id_parent_category = None):
		"""
			Method reponsible for saving categories to database.

			Input :
				- categories : list of hash representing categories
				- id_parent_category : if not None, this is the id of the parent category in the database.
		"""
		pass

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

	def get_uncomplete_products(self):
		"""
			This method retrieves products and promotion hat are not complete

			- Output :
				- products : [{'url':...}]
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
		pass

	def empty_database(self):
		pass

	def serialize(self, models):
		"""
			Input :
				- models : Queryset, list of models
			Output :
				- hash representing model with all database fields as keys
		"""
		models_hash = json.loads(serializers.serialize("json", models))
		for s in models_hash:
			s.update(s['fields'])
			s.update({'id': s['pk']})
			s.update({'id': s['pk']})
			del s['pk']
			del s['model']
			del s['fields']

		return models_hash

	def shut_down_category(self, category):
		"""
			If a category does not exist in the osm, set its argument exists to False
		"""
		if category is not None:
			category.exists = False
			category.save()
			# Getting all products associated with category and remove from m2m table
			if hasattr(category, 'newproduct_set'):
				c.newproduct_set.clear()
			elif hasattr(category, 'product_set'):
				c.newproduct_set.clear()