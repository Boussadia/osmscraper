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
		super(MonoprixScraper, self).__init__('http://courses.monoprix.com', MonoprixCrawler, MonoprixParser, MonoprixDatabaseHelper)

	def get_all_categories(self):
		"""
			Categories process, specific to child class.
		"""
		url = 'http://courses.monoprix.com/magasin-en-ligne/courses-en-ligne.html'
		categories, code = self.get_categories(url, level = 0)

		# Categories is a list of main categories
		# Cycle through these categories and keep going until level 3

		for i in xrange(0, len(categories)):
			main_category = categories[i]

			url = main_category['url']
			sub_categories, code = self.get_categories(url, level = 1)

			# Getting level 2 categories
			for j in xrange(0,len(sub_categories)):
				sub_category = sub_categories[j]
				url = sub_category['url']
				sub_categories_level_2, code = self.get_categories(url, level = 2)

				# Getting sub categories level 3
				for k in xrange(0, len(sub_categories_level_2)):
					sub_category_level_2 = sub_categories_level_2[k]
					url = sub_category_level_2['url']
					sub_categories_level_3, code = self.get_categories(url, level = 3)

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

	def get_categories(self, url, level = 0):
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

		if level > 1:
			return categories, 200

		# Getting main categories
		html, code = self.crawler.get(url)
		if code == 200:
			self.parser.set_html(html)
			categories = self.parser.get_categories(level = level)
			# Setting proper urls
			[ cat.update({'url': self.properurl(cat['url'])}) for cat in categories]
			# Save categories
			# categories = self.databaseHelper.save_categories(categories)
		else:
			print "Something went wrong when fetching main categories for Ooshop : code %d"%(code)

		return categories, code

	def get_list_products_for_category(self, category_url, location = 'default', save = False):
		"""
			For a category and a location, retrieve product list and save them.

			Input :
				- category_url (string) : url to a category parsed_page
				- location (string) : postal code of the location, 'default' -> no location
		"""
		# Setting location & initializing products
		self.set_location(location)
		products = []

		# Getting html
		html, code = self.crawler.get(category_url)

		if code == 200:
			self.parser.set_html(html)
			pagination = self.parser.get_pagination()

			for i in xrange(0,len(pagination)):
				page = pagination[i]
				if i == 0:
					# page already fetched, no need to fetch it again
					pass
				else:
					html, code = self.crawler.category_pagination(category_url, page)

				if code == 200:
					self.parser.set_html(html)
					products = products + self.parser.get_products()
				else:
					print "Something went wrong when fetching category page (%d) for Ooshop : code %d"%(i+1,code)

		else:
			print "Something went wrong when fetching category page for Ooshop : code %d"%(code)

		# Cleaning urls
		products = self.clean_urls_in_products(products)

		# Saing products
		if save:
			self.databaseHelper.save_products(products, None, None)
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
			product['brand_image_url'] = self.properurl(product['brand_image_url'])
			product['product_image_url'] = self.properurl(product['product_image_url'])
			
			if not product['is_product'] and product['is_promotion'] and product['promotion']['type'] == 'multi' and 'product_image_urls' in product['promotion']:
				# Setting proper full urls
				product['promotion']['product_image_urls'] = [ self.properurl(url) for url in product['promotion']['product_image_urls']]
			new_products.append(product)

		return new_products


	def get_product_info(self, product_url, location = 'default', save = False):
		"""
			Retrive complete information for product.

			Input : 
				- product_url (string) :  url of product to scrape
				- location (string) : postal code of the location, 'default' -> no location
			Output :
				- hash representing the product 
				- code (int) : was the request successfull (200 = OK)
		"""
		# Setting location 
		self.set_location(location)

		# Retrieve html page
		html, code = self.crawler.get(product_url)

		if code == 200:
			self.parser.set_html(html)
			product = self.parser.parse_product_full()

			# Clean urls
			scheme, netloc, path, params, query, fragment = urlparse(product_url)
			product['reference'] = parse_qs(query)['NOEUD_IDFO'][0]
			product['url'] = product_url
			[product] = self.clean_urls_in_products([product])

			# save product in database
			if save:
				self.databaseHelper.save_products([product], None, None)
			else:
				return product

		else:
			print 'Error while retrieving product page : error %d'%(code)
			return None

	def is_served_area(self, code_postal = 'default'):
		"""
			This method checks if a given area is served by ooshop.

			Input :
				- code_postal (string) : french postal code of a city.
			Output:
				- boolean : True -> served, False -> not served
				- code : was the request successfull? (200 = OK)
		"""
		is_served = False

		# Verification url
		url = 'http://www.ooshop.com/courses-en-ligne/WebForms/Utilisateur/VerifEligibilite.aspx'
		html, code = self.crawler.get(url)
		if code == 200:
			self.parser.set_html(html)
			form_data = self.parser.get_form_values()
			# Setting postal code argument to the one povided & other necessary post value
			form_data['ctl00$cphC$elig$tbCp'] = code_postal
			form_data['ctl00$sm'] = 'ctl00$sm|ctl00$cphC$elig$bEli'
			form_data['__EVENTTARGET'] = ''
			form_data['__EVENTARGUMENT'] = ''
			form_data['__LASTFOCUS'] = ''
			form_data['ctl00$xCoordHolder'] = 0
			form_data['ctl00$yCoordHolder'] = 281

			# Deleting unecessary post argument
			del form_data['ctl00$cphC$elig$ValiderEmail2']
			del form_data['ctl00$headerCtrl$btOK']
			del form_data['ctl00$cphC$elig$lv$LoginButton']
			del form_data['ctl00$Perso$ucAu$ValiderEmail']
			del form_data['ctl00$Perso$ucAu$SubmitButton']
			del form_data['ctl00$Perso$ucAu$lv$LoginButton']
			del form_data['ctl00$ucDetProd$AjoutPanier1$btPan']

			# geting response
			html, code = self.crawler.post(url, data = form_data)
			
			if code == 200:
				# Parsing html
				self.parser.set_html(html)
				is_served = self.parser.get_eligibility()
			else:
				print 'Error %d'%(code)

		else:
			print 'Something went wrong : error %d'%(code)

		return is_served, code


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
