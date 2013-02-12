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