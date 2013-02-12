#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from urlparse import urlparse, parse_qs, urlunparse

from scrapers.base.basescraper import BaseScraper
from scrapers.auchan.auchanparser import AuchanParser
from scrapers.auchan.auchancrawler import AuchanCrawler
from scrapers.auchan.auchandatabasehelper import AuchanDatabaseHelper

class AuchanScraper(BaseScraper):
	def __init__(self):
		super(AuchanScraper, self).__init__('http://www.refonte.auchandirect.fr', AuchanCrawler, AuchanParser, AuchanDatabaseHelper)

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



	def what_to_do_next(self):
		"""
			Defines the logic of the scraper.
		"""
		pass