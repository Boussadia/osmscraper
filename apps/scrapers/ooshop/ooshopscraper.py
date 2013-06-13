#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from urlparse import urlparse, parse_qs, urlunparse

from apps.scrapers.base.basescraper import BaseScraper
from apps.scrapers.ooshop.ooshopparser import OoshopParser
from apps.scrapers.ooshop.ooshopcrawler import OoshopCrawler
from apps.scrapers.ooshop.ooshopdatabasehelper import OoshopDatabaseHelper

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
			# Setting proper urls
			[ cat.update({'url': self.set_proper_url_for_category(cat['url'])}) for cat in categories]
			# Save categories
			categories = self.databaseHelper.save_categories(categories)
		else:
			print "Something went wrong when fetching main categories for Ooshop : code %d"%(code)

		# Categories is a list of main categories and sub categories level 1
		# Cycle through level 1 categories keep going untill level 3

		for i in xrange(0, len(categories)):
			main_category = categories[i]
			# Setting proper urls
			[ cat.update({'url': self.set_proper_url_for_category(cat['url'])}) for cat in main_category['sub_categories']]

			for j in xrange(0, len(main_category['sub_categories'])):
				level_1_category = main_category['sub_categories'][j]
				url = level_1_category['url']
				html, code = self.crawler.get(url)
				if code == 200:
					self.parser.set_html(html)
					level_1_category['sub_categories'] = self.parser.get_categories(level = 2)
					# Setting proper urls
					[ cat.update({'url': self.set_proper_url_for_category(cat['url'])}) for cat in level_1_category['sub_categories']]
					# Save categories
					[level_1_category] = self.databaseHelper.save_categories([level_1_category], main_category['id'])

					# We have to fetch sub categories level 3 here because of the way Ooshop website works
					for k in xrange(0, len(level_1_category['sub_categories'])):
						level_2_category = level_1_category['sub_categories'][k]
						url = level_2_category['url']
						html, code = self.crawler.get(url)
						if code == 200:
							self.parser.set_html(html)
							level_2_category['sub_categories'] = self.parser.get_categories(level = 3)
							# Setting proper urls
							[ cat.update({'url': self.set_proper_url_for_category(cat['url'])}) for cat in level_2_category['sub_categories']]
							# Save categories
							[level_2_category] = self.databaseHelper.save_categories([level_2_category], level_1_category['id'])
							level_2_category['sub_categories'] = self.databaseHelper.save_categories(level_2_category['sub_categories'], level_2_category['id'])
							level_1_category['sub_categories'][k] = level_2_category
						else:
							print "Something went wrong when fetching level 3 categories for Ooshop"

					# Save categories
					# level_1_category['sub_categories'] = self.databaseHelper.save_categories(level_1_category['sub_categories'], level_1_category['id'])					
				else:
					print "Something went wrong when fetching level 2 categories for Ooshop"
	
	def set_proper_url_for_category(self, category_url):
		"""
			We need to add /courses-en-ligne/ to category page because brand filter request wont work otherwise.
		"""
		url = self.properurl(category_url)
		if '/courses-en-ligne/' not in url:
			splitted = url.split(self.base_url)
			splitted.insert(0, '/courses-en-ligne')
			url = self.base_url+''.join(splitted)
		return url



	def get_list_products_for_category(self, category_url, location = 'default', save = False):
		"""
			For a category and a location, retrieve product list and save them.

			Input :
				- category_url (string) : url to a category parsed_page
				- location (string) : postal code of the location, 'default' -> no location
		"""
		# Setting location, & initializing products
		is_LAD, code = self.set_location(location)
		category_url = self.set_proper_url_for_category(category_url)

		if is_LAD and code == 200:
			shipping_area = self.databaseHelper.get_shipping_area(location)
		else:
			shipping_area = None
		products = []

		# Getting html
		html, code = self.crawler.get(category_url)

		if code == 200:
			self.parser.set_html(html)

			# Getting brand filter values
			brands = self.parser.get_brands_values_in_category_page()

			if brands is not None:

				for i in xrange(0,len(brands)):
					brand = brands[i]
					fetched_products = []
					# Getting html corresponding to filter
					html, code = self.crawler.brand_filter(category_url, brand)

					if code == 200:
						# Getting pagination
						self.parser.set_html(html)
						pagination = self.parser.get_pagination()

						for j in xrange(0,len(pagination)):
							# Going through every page and get products
							page = pagination[j]
							if j == 0:
								# page already fetched, no need to fetch it again
								pass
							else:
								html, code = self.crawler.category_pagination(category_url, page)

							if code == 200:
								self.parser.set_html(html)
								tmp = self.parser.get_products()
								for k in xrange(0, len(tmp)):
									tmp[k]['parent_brand'] = brand['value']
								fetched_products = fetched_products + tmp
								# Setting brand name to products
							else:
								print "Something went wrong when fetching category page (%d) and brand %s for Ooshop : code %d"%(j+1, brand['name'],code)
						# Updating products list
						products = products + fetched_products
					else:
						print "Something went wrong when fetching brand page (%s) for Ooshop : code %d"%(brand['name'],code)
		else:
			print "Something went wrong when fetching category page for Ooshop : code %d"%(code)

		# Cleaning urls
		products = self.clean_urls_in_products(products)

		# Saing products
		if save:
			# Getting category
			category = self.databaseHelper.get_category_by_url(category_url)
			if category and len(products) == 0:
				# Category does not exist anymore
				self.databaseHelper.shut_down_category(category)
			elif category:
				self.databaseHelper.save_products(products, category.id, shipping_area)
			else:
				self.databaseHelper.save_products(products, None, shipping_area)
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
			if 'brand_image_url' in product:
				product['brand_image_url'] = self.properurl(product['brand_image_url'])
			if 'product_image_url' in product:
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
		# Setting location, & initializing products
		is_LAD, code = self.set_location(location)

		if is_LAD and code == 200:
			shipping_area = self.databaseHelper.get_shipping_area(location)
		else:
			shipping_area = None

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

		else:
			print 'Error while retrieving product page : error %d'%(code)
			product = {
				'is_available': False,
				'exists': False,
				'url': product_url,
				'reference': product_url.split('-')[-1]
				}

		[product] = self.clean_urls_in_products([product])

		# save product in database
		if save:
			self.databaseHelper.save_products([product], None, shipping_area)
		else:
			return product

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
		# Clearing cookies
		self.crawler.empty_cookie_jar()

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

	def login_user(self, user_email = 'ahmed.boussadia@hotmail.fr', password = '2asefthukom,3'):
		"""
			This method checks if a given area is served by ooshop.

			Input :
				- code_postal (string) : french postal code of a city.
			Output:
				- boolean : True -> served, False -> not served
				- code : was the request successfull? (200 = OK)
		"""
		is_logued = False

		# Verification url
		url = 'http://www.ooshop.com/courses-en-ligne/WebForms/Utilisateur/VerifEligibilite.aspx'
		html, code = self.crawler.get(url)
		if code == 200:
			self.parser.set_html(html)
			form_data = self.parser.get_form_values()
			# Setting postal code argument to the one povided & other necessary post value
			form_data['ctl00$sm'] = 'ctl00$sm|ctl00$cphC$elig$lv$LoginButton'
			form_data['ctl00$cphC$elig$lv$utilisateur'] = user_email
			form_data['ctl00$cphC$elig$lv$mot_pass'] = password
			form_data['ctl00$cphC$elig$lv$LoginButton'] = 'VALIDER'
			form_data['__EVENTTARGET'] = ''
			form_data['__EVENTARGUMENT'] = ''
			form_data['__LASTFOCUS'] = ''
			form_data['ctl00$xCoordHolder'] = 0
			form_data['ctl00$yCoordHolder'] = 281
			form_data['ctl00$ucDetProd$AjoutPanier1$nbrProduit'] = 1

			# Deleting unecessary post argument
			del form_data['ctl00$Perso$ucAu$SubmitButton']
			del form_data['ctl00$Perso$ucAu$ValiderEmail']
			del form_data['ctl00$headerCtrl$btOK']
			del form_data['ctl00$cphC$elig$ValiderEmail2']
			del form_data['ctl00$ucDetProd$AjoutPanier1$btPan']
			del form_data['ctl00$cphC$elig$bEli']
			del form_data['ctl00$Perso$ucAu$lv$LoginButton']

			# geting response
			html, code = self.crawler.login_user(url, data = form_data)

			if code == 200:
				# Going to profile page in order to check if user loged in
				url_profile = 'http://www.ooshop.com/courses-en-ligne/WebForms/Utilisateur/MonCompte.aspx'
				html, code = self.crawler.get(url_profile)
				self.parser.set_html(html)
				is_logued =  self.parser.is_logued()
				# Parsing html
				self.parser.set_html(html)
				# is_served = self.parser.get_eligibility() TOBE DONE : check if user logedin
			else:
				print 'Error %d'%(code)

		else:
			print 'Something went wrong : error %d'%(code)

		return is_logued, code

	def import_cart(self, user_email = 'ahmed.boussadia@hotmail.fr', password = '2asefthukom,3'):
		"""
			Imports cart for a ooshop user.
		"""
		cart = []

		# Clearing cookies
		self.crawler.empty_cookie_jar()

		# log user
		is_logued, code = self.login_user(user_email, password)

		if code == 200:
			if is_logued:
				# user loged, got ot cart page and extract cart from parser
				url_cart = 'http://www.ooshop.com/courses-en-ligne/WebForms/Panier/ValidationPanierHorsTunnel.aspx'
				html, code = self.crawler.get(url_cart)
				self.parser.set_html(html)
				# Getting pagination
				self.parser.set_html(html)
				pagination = self.parser.get_pagination()
				options = self.parser.get_form_values()

				for j in xrange(0,len(pagination)):
					# Going through every page and get products
					page = pagination[j]

					if j == 0:
						# page already fetched, no need to fetch it again
						pass
					else:
						html, code = self.crawler.cart_pagination(url_cart, page, options)

					if code == 200:
						self.parser.set_html(html)
						cart = cart + self.parser.get_products_in_cart()
					else:
						print "Something went wrong when fetching category page (%d) and brand %s for Ooshop : code %d"%(j+1, brand['name'],code)
				# Updating products list				
				return cart, code, is_logued
			else:
				# user not loged
				return cart, code, is_logued
		else:
			return cart, code, is_logued

	def export_cart(self, products, user_email = 'ahmed.boussadia@hotmail.fr', password = '2asefthukom,3'):
		"""
			Exports cart for a ooshop user.
		"""
		
		# Clearing cookies
		self.crawler.empty_cookie_jar()

		# log user
		is_logued, code = self.login_user(user_email, password)

		if code == 200:
			if is_logued:
				# Cycle throug every product and put it in cart
				for product in products:
					url_product = product['url']
					html, code = self.crawler.get(url_product)
					self.parser.set_html(html)
					# Getting options
					options = self.parser.get_form_values()
					html, code = self.crawler.put_product_in_cart(product, options)


	def is_available(self, product_url):
		"""
			This method checks if the product is still available in the osm website
		"""
		pass
