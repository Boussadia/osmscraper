#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from urlparse import urlparse, parse_qs, urlunparse

from scrapers.base.basescraper import BaseScraper
from scrapers.ooshop.ooshopparser import OoshopParser
from scrapers.ooshop.ooshopcrawler import OoshopCrawler
from scrapers.ooshop.ooshopdatabasehelper import OoshopDatabaseHelper

class OoshopScraper(BaseScraper):
	"""
		docstring for OoshopScraper
	"""
	def __init__(self):
		super(OoshopScraper, self).__init__('http://www.ooshop.com', OoshopCrawler, OoshopParser, OoshopDatabaseHelper)

	def get_all_categories(self):
		"""
			Categories process, specific to child class.
		"""
		url = self.base_url
		categories = []

		# Getting main and sub categories level 1
		html, code = self.crawler.get(url)
		if code == 200:
			self.parser.set_html(html)
			categories = self.parser.get_categories(level = 0)
		else:
			print "Something went wrong when fetching main categories for Ooshop : code %d"%(code)

		# Categories is a list of main categories and sub categories level 1
		# Cycle through level 1 categories keep going till level 3

		for i in xrange(0, len(categories)):
			main_category = categories[i]

			for j in xrange(0, len(main_category['sub_categories'])):
				level_1_category = main_category['sub_categories'][j]
				url = self.base_url + '/' + level_1_category['url']
				html, code = self.crawler.get(url)
				if code == 200:
					self.parser.set_html(html)
					level_1_category['sub_categories'] = self.parser.get_categories(level = 2)

					# We have to fetch sub categories level 3 here because of the way Ooshop website works
					for k in xrange(0, len(level_1_category['sub_categories'])):
						level_2_category = level_1_category['sub_categories'][k]
						url = self.base_url + '/' + level_2_category['url']
						html, code = self.crawler.get(url)
						if code == 200:
							self.parser.set_html(html)
							level_2_category['sub_categories'] = self.parser.get_categories(level = 3)
						else:
							print "Something went wrong when fetching level 3 categories for Ooshop"

				else:
					print "Something went wrong when fetching level 2 categories for Ooshop"
		
		# Here we pass the categories list to the databasehelper to be saved
		# TO DO

	def get_list_products_for_category(self, category_url, location = 'default'):
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

		print len(products)


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
			Retrive complete information for product. Independent from localisation.

			Input : 
				- product_url (string) :  url of product to scrape
			Output :
				- hash representing the product 
				- code (int) : was the request successfull (200 = OK)
		"""
		# First, retrieve html page
		html, code = self.crawler.get(product_url)

		if code == 200:
			self.parser.set_html(html)
			product = self.parser.parse_product_full()

			# Adding reference to product hash
			if product['is_product']:
				scheme, netloc, path, params, query, fragment = urlparse(product_url)
				product['reference'] = parse_qs(query)['NOEUD_IDFO'][0]
				product['url'] = product_url

				# Setting proper full urls
				product['brand_image_url'] = urlunparse((scheme, netloc, product['brand_image_url'], '', '', ''))
				product['product_image_url'] = urlunparse((scheme, netloc, product['product_image_url'], '', '', ''))
			print product
			# TO DO : save product in database
		else:
			print 'Error while retrieving product page : error %d'%(code)

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
			return True, 200

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