#!/usr/bin/python
# -*- coding: utf-8 -*-

class BaseScraper(object):
	"""
		This class is responsible for coordianting the actions of the crawler, parser and databasehelper.

		It includes the following static methods that are celery tasks (to be implemented by a child class):
			- get_all_categories : retrieve all the architecture of the categories
			- get_all_products : retireve all products, 
			- get_localized_product : retrieve products for a certain localization
			- get_product_info : retireve full product information (independant form localization)
			- is_available : checks if a product desapeared from the osm website
			- what_to_do_next : tasks that defines the logic of the scraper tasks to start.
	"""

	def __init__(self, base_url, Crawler_class, Parser_class, DatabaseHelper_class):
		self.base_url = base_url
		self.crawler = Crawler_class()
		self.parser = Parser_class()
		self.databaseHelper = DatabaseHelper_class()

	def get_all_categories(self):
		"""
			Categories process, specific to child class.
		"""
		pass

	def get_all_products(self):
		"""
			Retrives all possible localisation, retrieves all categories and fetches all products for
			each localisation and saves them.
		"""
		pass

	def get_localized_product(self, localisation):
		pass



	def get_product_info(self, product_url):
		"""
			Retrive complete information for product.
		"""
		pass

	def is_available(self, product_url):
		"""
			This method checks if the product is still available in the osm website
		"""
		pass

	def what_to_do_next(self):
		"""
			Defines the logic of the scraper.
		"""
		pass