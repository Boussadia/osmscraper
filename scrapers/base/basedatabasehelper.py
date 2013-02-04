#!/usr/bin/python
# -*- coding: utf-8 -*-

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

	def save_products(self, products, id_parent_category):
		"""
			Method responsible for saving products to database
		"""

	def get_categories(self):
		"""
			Method that retrieves all categories in a hash.

			Output :
				- categories : list of hashs representing categories.
		"""