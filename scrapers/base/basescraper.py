#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time

from scrapers.base.cities import cities
from urlparse import urlparse, parse_qs, urlunparse

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

	def set_location(self, code_postal = 'default'):
		"""
			Sets crawler location to the one defined. Clears cookies first.

			Input : 
				- code_postal (string) : french postal code of a city.
			Output :
				- boolean : True -> served, False -> not served
				- code : was the request successfull? (200 = OK)

		"""
		# Clearing cookie jar
		self.crawler.empty_cookie_jar()
		if re.match(r'(\d{5})', code_postal):
			return self.is_served_area(code_postal)
		else:
			# Location not abiding by postal code standard
			return False, -1

	def is_served_area(self, code_postal = 'default'):
		"""
			This method checks if a given area is served by ooshop.

			Input :
				- code_postal (string) : french postal code of a city.
			Output:
				- boolean : True -> served, False -> not served
				- code : was the request successfull? (200 = OK)
		"""
		pass

	def build_shipping_area(self):
		"""
			Building shipping area from cities.
		"""
		shipping_areas = []
		for postal_code, city_name in cities:
			is_shipping_area, code = self.is_served_area(postal_code)
			if code == 200 and is_shipping_area:
				# Passing result to database helper
				self.databaseHelper.save_shipping_areas([{
					'is_shipping_area': True,
					'name': city_name,
					'postal_code': postal_code
				}])
			if is_shipping_area:
				print 'City : %s (%s) is OK'%(city_name, postal_code)
			else:
				print 'City : %s (%s) is NOT OK'%(city_name, postal_code)
			time.sleep(1) # In order not to flood server, 1s temporisation

		# Adding default location (non set) to shipping areas
		self.databaseHelper.save_shipping_areas([{
					'is_shipping_area': False,
					'name': '',
					'postal_code': '',
				}])


	def what_to_do_next(self):
		"""
			Defines the logic of the scraper.
		"""
		pass



	def properurl(self, url_to_format):
		"""
			Formating a proper url :
				base_url = 'http://www.example.com', url_to_format = 'path/to/page' -> 'http://www.example.com/path/to/page'
				base_url = 'http://www.example.com', url_to_format = 'http://www.example.com/path/to/page' -> 'http://www.example.com/path/to/page'
		"""
		base_url = self.base_url
		scheme_base, netloc_base, path_base, params_base, query_base, fragment_base = urlparse(base_url)
		scheme, netloc, path, params, query, fragment = urlparse(url_to_format)

		return urlunparse((scheme_base, netloc_base, path, params, query, fragment))