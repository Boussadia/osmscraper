#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2

from bs4 import BeautifulSoup

import re

class OSMScraper(object):
	"""docstring for OSMParser"""
	def __init__(self, url):
		super(OSMScraper, self).__init__()
		self.__base_url__ = url
		self.__categories__= {}

	def fetch_html(self, url=""):
		if url.find(self.get_base_url())>-1:
			pass
		else:
			url = self.get_base_url()+"/"+url
		print "Fetching page from "+url
		response = urllib2.urlopen(url)
		html = response.read()
		print "Page Fetched for "+response.geturl()
		response.close()
		return html

	def get_parsed_page_for_url(self, url=""):
		html_page = self.fetch_html(url)
		parsed_page = BeautifulSoup(html_page)
		return parsed_page

	def get_base_url(self):
		return self.__base_url__

	def get_categories(self):
		return self.__categories__

	def set_categories(self, categories):
		self.__categories__ = categories

	def get_menu():
		"""
			Method to overide by child class.
		"""
		pass