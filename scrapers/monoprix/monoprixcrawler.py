#!/usr/bin/python
# -*- coding: utf-8 -*-

from scrapers.base.basecrawler import BaseCrawler

class MonoprixCrawler(BaseCrawler):

	def __init__(self):
		super(MonoprixCrawler, self).__init__()
		# Monoprix does mot like Python user agemt, so we are cheating a little bit ...
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; Intel Mac OS X 10.6; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'
		self.browser.addheaders = [('User-agent', user_agent)]		

	def brand_filter(self, brand_value):
		"""
			This method is the equivalent of filtering products by brand name in a category page

			Input :
				- brand_value (string) : brand value in option tag
			Output:
				- code : page retrieved from wed?
				- html : fetched html
		"""
		url = 'http://courses.monoprix.fr/productlist.productslist.marqueslistfield:selectchange2/'+brand_value
		return self.get(url)