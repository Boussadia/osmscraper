#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from urlparse import urlparse, parse_qs, urlunparse

from scrapers.base.basescraper import BaseScraper
from scrapers.monoprix.monoprixparser import MonoprixParser
from scrapers.monoprix.monoprixcrawler import MonoprixCrawler
from scrapers.monoprix.monoprixdatabasehelper import MonoprixDatabaseHelper

class MonoprixScraper(BaseScraper):
	"""
		docstring for MonoprixScraper
	"""
	def __init__(self):
		super(MonoprixScraper, self).__init__('http://courses.monoprix.fr', MonoprixCrawler, MonoprixParser, MonoprixDatabaseHelper)

	def get_all_categories(self):
		"""
			Categories process, specific to child class.
		"""
		url = self.base_url
		categories, code = self.get_categories(url, level = 0)
		categories = self.databaseHelper.save_categories(categories)

		# Categories is a list of main categories
		# Cycle through these categories and keep going until level 3

		for i in xrange(0, len(categories)):
			main_category = categories[i]

			url = main_category['url']
			sub_categories, code = self.get_categories(url, level = 1, id_parent_category = main_category['id'])

			# Getting level 2 categories
			for j in xrange(0,len(sub_categories)):
				sub_category = sub_categories[j]
				url = sub_category['url']
				sub_categories_level_2, code = self.get_categories(url, level = 2, id_parent_category = sub_category['id'])

				# Getting sub categories level 3
				for k in xrange(0, len(sub_categories_level_2)):
					sub_category_level_2 = sub_categories_level_2[k]
					url = sub_category_level_2['url']
					sub_categories_level_3, code = self.get_categories(url, level = 3, id_parent_category = sub_category_level_2['id'] )

					# Updating sub categories level 2
					sub_category_level_2['sub_categories'] = sub_categories_level_3
					sub_categories_level_2[k] = sub_category_level_2


				# Updating sub category level 1
				sub_category['sub_categories'] = sub_categories_level_2
				sub_categories[j] = sub_category

			# Updating main category
			main_category['sub_categories'] = sub_categories
			categories[i] = main_category

		return categories

	def get_categories(self, url, level = 0, id_parent_category = None):
		"""
			Method for getting sub categories fr url.

			Input :
				- url (string) : url of category 
				- level (int) : level of categories to extract

			Output :
				- categories (list of hash) : list of sub categories found
				- code (int) : http code of the request 

		"""
		categories = []

		# Getting main categories
		html, code = self.crawler.get(url)
		if code == 200:
			self.parser.set_html(html)
			categories = self.parser.get_categories(level = level)
			# Setting proper urls
			[ cat.update({'url': self.properurl(cat['url'])}) for cat in categories]
			# Save categories
			categories = self.databaseHelper.save_categories(categories, id_parent_category)
		else:
			print "Something went wrong when fetching main categories for Monoprix : code %d"%(code)

		return categories, code

	def get_list_products_for_category(self, category_url, location = {}, save = False):
		"""
			For a category and a location, retrieve product list and save them.

			Input :
				- category_url (string) : url to a category parsed_page
				- location (hash) : store as a hash ({'city_name': ..., 'postal_code':..., 'address': ...})
		"""
		# Setting location, getting category form datastore & initializing products
		is_LAD, code = self.set_location(location)

		if is_LAD and code == 200:
			store = self.databaseHelper.get_store(location)
		else:
			store = None

		# Category
		categories = self.databaseHelper.get_categories({'url': category_url})
		if len(categories)>0:
			category = categories[0]['db_entity']
		else:
			category = None
		products = []

		# Getting html
		html, code = self.crawler.get(category_url)
		

		if code == 200:
			self.parser.set_html(html)
			brands = self.parser.get_brands_values_in_category_page()

			for i in xrange(0,len(brands)):
				brand = brands[i]
				html, code = self.crawler.brand_filter(brand['value'])

				if code == 200:
					self.parser.set_html(html)
					# are all the products on in this page ?
					current_page_all_products, url_all_products = self.parser.pagination_link_all()
					if not current_page_all_products:
						products = products + self.parser.get_products()
					else:
						html, code = self.crawler.get(url_all_products)
						if code == 200:
							html, code = self.crawler.brand_filter(brand['value'])
							if code == 200:
								self.parser.set_html(html)
								products = products + self.parser.get_products()
							else:
								print "Something went wrong when fetching category page for Monoprix : code %d"%(code)
						else:
							print "Something went wrong when fetching category page for Monoprix : code %d"%(code)
				else:
					print "Something went wrong when fetching category page (%d) for Monoprix : code %d"%(i+1,code)
				# Setting brand name to product
				for j in xrange(0, len(products)):
					products[j]['brand'] = brand['name']
		else:
			print "Something went wrong when fetching category page for Monoprix : code %d"%(code)

		# Cleaning urls
		products = self.clean_urls_in_products(products)

		# Saing products
		if save:
			if category:
				self.databaseHelper.save_products(products, category.id, store)
			else:
				self.databaseHelper.save_products(products, None, store)
		else:
			return products


	def get_all_products(self):
		"""
			Retrives all possible localisation, retrieves all categories and fetches all products for
			each localisation and saves them.
		"""
		pass

	def clean_urls_in_products(self, products):
		"""
			Clean all urls in products list

			Input :
				- products (list hash) : products

			Output :
				- the same list of products but with clean urls
		"""
		new_products = []
		for product in products:
			# Clean urls
			product['url'] = self.properurl(product['url'])
			product['product_image_url'] = self.properurl(product['product_image_url'])
			
			if not product['is_product'] and product['is_promotion'] and product['promotion']['type'] == 'multi' and 'product_image_urls' in product['promotion']:
				# Setting proper full urls
				product['promotion']['references'] = [ self.properurl(url) for url in product['promotion']['product_image_urls']]
			new_products.append(product)

		return new_products


	def get_product_info(self, product_url, location = {}, save = False):
		"""
			Retrieve complete information for product.

			Input : 
				- product_url (string) :  url of product to scrape
				- location (hash) : store as a hash ({'city_name': ..., 'postal_code':..., 'address': ...})
			Output :
				- hash representing the product 
				- code (int) : was the request successfull (200 = OK)
		"""
		# Setting location 
		is_LAD, code = self.set_location(location)

		if is_LAD and code == 200:
			store = self.databaseHelper.get_store(location)
		else:
			store = None


		# Retrieve html page
		html, code = self.crawler.get(product_url)

		if code == 200:
			self.parser.set_html(html)
			product = self.parser.parse_product_full()

			# Clean urls
			product['reference'] = product_url.split('-')[-1]
			product['url'] = product_url
			[product] = self.clean_urls_in_products([product])

			# save product in database
			if save:
				self.databaseHelper.save_products([product], None, store)
			else:
				return product

		elif code == 404:
			product = {
				'is_available': False,
				'url': product_url,
				'reference': product_url.split('-')[-1]
				}

			# save product in database
			if save:
				self.databaseHelper.save_products([product], None, store)
			else:
				return product
		else:
			print 'Error while retrieving product page : error %d'%(code)
			return None

	def is_served_area(self, location):
		"""
			This method checks if a given area is served by monoprix.

			Input :
				- location (hash) : store as a hash ({'city_name': ..., 'postal_code':..., 'address': ...})
			Output:
				- boolean : True -> served, False -> not served
				- code : was the request successfull? (200 = OK)
		"""
		is_served = False
		code = 500

		url = self.base_url

		html, code = self.crawler.get(url)

		if code == 200:
			# Getting form data 
			self.parser.set_html(html)
			form_data = self.parser.get_postal_code_form_data()
			data = form_data['data']
			url = self.properurl(form_data['url'])

			data['enteredZipCode'] = location['postal_code']

			html, code = self.crawler.post(url, data)
			self.parser.set_html(html)
			data_delivery = self.parser.get_form_delivery_zone()

			if data_delivery['type'] == 'address':
				html, code = self.crawler.search_adress('%s, %s %s'%(location['address'].encode('utf8', 'replace'),location['postal_code'].encode('utf8', 'replace'), location['city_name'].encode('utf8', 'replace')))
				suggetions = self.parser.extract_suggested_addresses(html)
				[s.update({'url': self.properurl(s['url'])} )for s in suggetions]

				if len(suggetions) > 0:
					# There is at least one suggestion, select the first
					address = suggetions[0]

					# Now set this address
					html, code = self.crawler.set_address(address)
					self.parser.set_html(html)
					form_data = self.parser.get_form_delivery_zone()
					form_data['form']['url'] = self.properurl(form_data['form']['url'])
					html, code = self.crawler.set_delivery(form_data)
					if code == 200:
						is_served = True

			elif data_delivery['type'] == 'select':
				data_delivery['form']['url'] = self.properurl(data_delivery['form']['url'])
				if 'radiogroup' in data_delivery['form']['data'] and 'LAD' in data_delivery['form']['data']['radiogroup']:
					html, code = self.crawler.set_delivery(data_delivery)
					if code == 200:
						is_served = True
				else:
					is_served = False

		else:
			print 'Error while fetching base url of Monoprix (code = %d)'%(code)

		return is_served, code

	def set_location(self, location = {}):
		"""
			Sets crawler location to the one defined. Clears cookies first.

			Input : 
				- location (hash) : store as a hash ({'city_name': ..., 'postal_code':..., 'address': ...})
			Output :
				- boolean : True -> served, False -> not served
				- code : was the request successfull? (200 = OK)

		"""
		# Clearing cookie jar
		self.crawler.empty_cookie_jar()
		if 'city_name' in location and 'postal_code' in location and 'address' in location and re.match(r'(\d{5})', location['postal_code']):
			return self.is_served_area(location)
		# Location not abiding by postal code standard
		return False, -1

	def build_shipping_area(self):
		"""
			Building shipping area from stores.
		"""
		stores = self.databaseHelper.get_stores()

		for store in stores:
			print 'Store : %s, %s %s %s'%(store['name'], store['address'], store['city_name'], store['postal_code'])
			is_LAD, code = self.set_location(store)
			if code == 200 and is_LAD:
				print 'Is OK'
			elif code != 200:
				print 'Error code : %d'%(code)
			else:
				print 'Is NOT OK'

			if code == 200 and is_LAD != store['is_LAD']:
				store['is_LAD'] = is_LAD
				self.databaseHelper.save_stores([store])


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
