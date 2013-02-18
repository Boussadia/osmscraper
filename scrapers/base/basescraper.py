#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time
from datetime import datetime, timedelta, date
from urlparse import urlparse, parse_qs, urlunparse

from django.utils.timezone import utc

from scrapers.base.cities import cities

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

	def get_list_products_for_category(self, category_url, location = 'default', save = False):
		"""
			For a category and a location, retrieve product list and save them.

			Input :
				- category_url (string) : url to a category parsed_page
				- location (string) : postal code of the location, 'default' -> no location
		"""
		pass

	def get_all_products(self):
		"""
			Retrives all possible localisation, retrieves all categories and fetches all products for
			each localisation and saves them.
		"""
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
		if code_postal:
			# Clearing cookie jar
			self.crawler.empty_cookie_jar()
			if re.match(r'(\d{5})', code_postal):
				return self.is_served_area(code_postal)
			else:
				# Location not abiding by postal code standard
				return False, -1
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

	def build_shipping_area(self, reg_filter = None):
		"""
			Building shipping area from cities.

			Input : 
				- reg_filter : regexp in order to filter postal codes (it has to be previously compiled)
					i.e. : re.compile('94(\d{3})') -> one filter for cities in the 94 departement
		"""
		shipping_areas = []
		for postal_code, city_name in cities:
			is_matched = True
			if reg_filter:
				m = reg_filter.match(postal_code)
				if not m:
					is_matched = False

			if is_matched:
				is_shipping_area, code = self.is_served_area(postal_code)
				if code == 200 and is_shipping_area:
					# Passing result to database helper
					self.databaseHelper.save_shipping_areas([{
						'is_shipping_area': True,
						'name': city_name,
						'postal_code': postal_code
					}])
					print 'City : %s (%s) is OK'%(city_name, postal_code)
				if code == 200 and not is_shipping_area:
					print 'City : %s (%s) is NOT OK'%(city_name, postal_code)
					
				time.sleep(2) # In order not to flood server, 2s temporisation

		# Adding default location (non set) to shipping areas
		self.databaseHelper.save_shipping_areas([{
					'is_shipping_area': False,
					'name': 'DEFAULT',
					'postal_code': '00000',
				}])


	def what_to_do_next(self):
		"""
			Defines the logic of the scraper. (See Google Drive documentation for further explanation)
		"""
		# First are there categories stored?
		categories = self.databaseHelper.get_categories(options={'leaves':True})

		if len(categories) == 0:
			# No categories in database
			return {'type':'categories'}
		else:
			# Was the last time categories where updated more than 2 weeks ago?
			old_updated_categories = filter(lambda cat: cat['updated'].replace(tzinfo=None) + timedelta(days = 15)<datetime.today(), categories)
			if len(old_updated_categories) > 0:
				# Need to update categories list
				return {'type':'categories'}
			else:
				pass

		# Get complete products informations
		products = self.databaseHelper.get_uncomplete_products()
		if len(products)>0:
			return{
				'type': 'products',
				'products': products
			}

		# Getting all shipping areas

		shipping_areas = self.databaseHelper.get_shipping_areas()

		# Getting count of products for categories
		options = {
			'categories_id': [c['id'] for c in categories],
			'locations': [s['postal_code'] for s in shipping_areas],
		}
		# Building list of combinations between locations and categories [(category_id, location)]
		categories_locations_temp = [[(c['id'], s['postal_code']) for c in categories] for s in shipping_areas]
		categories_locations = []
		[categories_locations.extend(tup) for tup in categories_locations_temp]

		# Get products corresponding to filters
		products = self.databaseHelper.get_products(options=options)
		# For every product, build list of tuple of [(category_id, location)]
		products_categories_locations_temp_1 = [[[ (cid, pc) for cid in p['categories']] for pc in p['locations'] ]for p in products]
		products_categories_locations = []
		[[[ products_categories_locations.append(tup) for tup in p_2 if tup not in products_categories_locations]for p_2 in p_1] for p_1 in products_categories_locations_temp_1]
		
		# Now extract from categories_locations tuples of categories and locations to scrape:
		categories_locations_to_scrape = [tup for tup in categories_locations if tup not in products_categories_locations]

		# Is the list empty?
		if len(categories_locations_to_scrape)>0:
			# Building list to return
			# changing categories and location to speed up process
			categories = { c['id']:c for c in categories}
			return {
				'type': 'category_products',
				'categories': [{'url': categories[cat_id]['url'], 'location': cp} for cat_id, cp in categories_locations_to_scrape]
			}


		# Same process than above but filtering with time
		options.update({'before_date': datetime.utcnow().replace(tzinfo=utc)-timedelta(hours = 24)})
		categories_locations_temp = [[(c['id'], s['postal_code']) for c in categories] for s in shipping_areas]
		categories_locations = []
		[categories_locations.extend(tup) for tup in categories_locations_temp]

		# Get products corresponding to filters
		products = self.databaseHelper.get_products(options=options)
		# For every product, build list of tuple of [(category_id, location)]
		products_categories_locations_temp_1 = [[[ (cid, pc) for cid in p['categories']] for pc in p['locations'] ]for p in products]
		products_categories_locations = []
		[[[ products_categories_locations.append(tup) for tup in p_2 if tup not in products_categories_locations]for p_2 in p_1] for p_1 in products_categories_locations_temp_1]
		
		# Now extract from categories_locations tuples of categories and locations to scrape:
		categories_locations_to_scrape = [tup for tup in categories_locations if tup in products_categories_locations]

		# Is the list empty?
		if len(categories_locations_to_scrape)>0:
			# Building list to return
			# changing categories and location to speed up process
			categories = { c['id']:c for c in categories}
			return {
				'type': 'category_products',
				'categories': [{'url': categories[cat_id]['url'], 'location': cp} for cat_id, cp in categories_locations_to_scrape]
			}

		# TO DO : Check if products that were not fetch still exit on osm website

		# Nothing more to do, return task to execute in 1 hour
		return {
			'type': 'global',
			'delay': 3600 # seconds
		}

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

	def empty_database(self):
		self.databaseHelper.empty_database()