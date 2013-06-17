#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, json
from urlparse import urlparse, parse_qs, urlunparse

from apps.scrapers.base.basescraper import BaseScraper
from apps.scrapers.auchan.auchanparser import AuchanParser
from apps.scrapers.auchan.auchancrawler import AuchanCrawler
from apps.scrapers.auchan.auchandatabasehelper import AuchanDatabaseHelper

class AuchanScraper(BaseScraper):
	def __init__(self):
		super(AuchanScraper, self).__init__('http://www.auchandirect.fr', AuchanCrawler, AuchanParser, AuchanDatabaseHelper)

	def get_all_categories(self):
		"""
			Getting all categories from website and saving to database
		"""
		categories = []
		url = self.base_url

		html, code = self.crawler.get(url)

		if code == 200:
			self.parser.set_html(html)
			categories = self.parser.get_categories()
			for i in xrange(0, len(categories)):
				for j in xrange(0, len(categories[i]['sub_categories'])):
					categories[i]['sub_categories'][j]['url'] = self.properurl(categories[i]['sub_categories'][j]['url'])
					for k in xrange(0, len(categories[i]['sub_categories'][j]['sub_categories'])):
						categories[i]['sub_categories'][j]['sub_categories'][k]['url'] = self.properurl(categories[i]['sub_categories'][j]['sub_categories'][k]['url'])

			self.databaseHelper.save_categories(categories)

		else:
			print 'Could not scrape categories : error %d'%(code)

	def get_list_products_for_category(self, category_url, location = 'default', save = False):
		"""
			For a category and a location, retrieve product list and save them.

			Input :
				- category_url (string) : url to a category parsed_page
				- location (string) : postal code of the location, 'default' -> no location
		"""
		# Setting location, getting category form datastore & initializing products
		is_LAD, code = self.set_location(location)

		if is_LAD and code == 200:
			shipping_area = self.databaseHelper.get_shipping_area(location)
		else:
			shipping_area = None

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
			tags = self.parser.get_tags()

			for i in xrange(0,len(tags)):
				tags[i]['url'] = self.properurl(tags[i]['url'])
				tag = tags[i]
				html, code = self.crawler.category_tag(tag)

				if code == 200:
					self.parser.set_html_from_tag(html)
					filtered_products = self.parser.get_products()
					[ p.update({'tag':tag}) for p in filtered_products]
					products = products + filtered_products
				else:
					print "Something went wrong when fetching category page (%d) for Auchan : code %d"%(i+1,code)

			if len(tags) == 0:
				# Sometimes, there are no tags in a category page
				products = self.parser.get_products()

		else:
			print "Something went wrong when fetching category page for Auchan : code %d"%(code)

		#Cleaning urls
		products = self.clean_urls_in_products(products)

		#Saing products
		if save:
			if len(products) == 0:
				# Category does not exist anymore
				self.databaseHelper.shut_down_category(category)
			else:
				self.databaseHelper.save_products(products, category, shipping_area)
		else:
			return products




	def get_all_products(self):
		"""
			Retrives all possible localisation, retrieves all categories and fetches all products for
			each localisation and saves them.
		"""
		pass


	def get_product_info(self, product_url, location = 'default', save = False):
		"""
			Retrive complete information for product.
		"""
		# Setting location, getting category form datastore & initializing products
		is_LAD, code = self.set_location(location)

		if is_LAD and code == 200:
			shipping_area = self.databaseHelper.get_shipping_area(location)
		else:
			shipping_area = None

		product = {}
		html, code = self.crawler.get(product_url)

		if code == 200:
			self.parser.set_html(html)
			product = self.parser.parse_product_full()
			product['url'] = product_url
			product['reference'] = product_url.split('/')[-1].split(';jsessionid=')[0]
			[product] = self.clean_urls_in_products([product])
		else:
			print 'Error while fetching product : %d'%(code)
			product = {
				'is_available': False,
				'exists': False,
				'url': product_url,
				'reference': product_url.split('-')[-1]
				}

		#Saving product
		if save:
			self.databaseHelper.save_products([product], None, shipping_area)
		else:
			return product

	def is_available(self, product_url):
		"""
			This method checks if the product is still available in the osm website
		"""
		pass

	def is_served_area(self, code_postal = 'default'):
		"""
			This method checks if a given area is served by ooshop.

			Input :
				- code_postal (string) : french postal code of a city.
			Output:
				- boolean : True -> served, False -> not served
				- code : was the request successfull? (200 = OK)
		"""
		# Only proceed if available postal code
		if not re.match(r'(\d{5})',code_postal):
			return False, -1

		is_served_area = False
		url = self.base_url
		self.crawler.empty_cookie_jar()
		html, code = self.crawler.get(url)

		if code == 200:
			self.parser.set_html(html)
			form_data = self.parser.get_form_postal_code()
			url = self.properurl(form_data['url'])
			data = form_data['data']
			data['storeSearch'] = code_postal
			html, code = self.crawler.post(url, data)
			cookie = self.crawler.get_cookie(name = 'shop')
			if cookie != {}:
				# Cookie found -> is a served area
				is_served_area = True

		return is_served_area, code


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
			product['url'] = self.properurl(product['url']).split(';jsessionid=')[0]
			if 'product_image_url' in product:
				product['product_image_url'] = self.properurl(product['product_image_url']).split(';jsessionid=')[0]
			new_products.append(product)

		return new_products


	def login_user(self, user_email = 'ahmed.boussadia@hotmail.fr', password = '2asefthukom3'):
		"""
		"""
		is_logued = False

		# First get cookies by going to home page
		html, code = self.crawler.get('http://www.auchandirect.fr/Accueil');

		if code == 200:
			self.parser.set_html(html)

			# Getting pop up for login 
			response, code = self.crawler.get_login_popup()
			if code == 200:

				# get html from json
				response_hash = json.loads(response)
				pop_up_html = response_hash['zones']['secondPopupZone']
				self.parser.set_html(pop_up_html)

				# Now parsing form data to get relevant information from html
				form_data = self.parser.get_form_login()

				form_data['form']['inputLogin'] = user_email
				form_data['form']['inputPwd'] = password

				response, code = self.crawler.login_user(form_data)

				response_hash = json.loads(response)

				if 'redirectURL' in response_hash and 'Accueil' in response_hash['redirectURL']:
					return True, code
			else:
				return is_logued, code	
			
		else:
			return is_logued, code
