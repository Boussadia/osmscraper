#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2

from bs4 import BeautifulSoup

import re
import time

class OSMScraper(object):
	"""docstring for OSMParser"""
	MAX_NETWORK_FAILURE_TRIES = 10

	def __init__(self, url):
		super(OSMScraper, self).__init__()
		self.__base_url__ = url
		self.__categories__= {}
		self.__network_failures_retry__ = 0

	def fetch_html(self, url=""):
		try:
			if url.find(self.get_base_url())>-1:
				pass
			else:
				if len(url)>0:
					if url[0] != '/':
						url = self.get_base_url()+"/"+url
					else:
						url = self.get_base_url()+url
				else:
					url = self.get_base_url()
			
			print "Fetching page from "+url
			response = urllib2.urlopen(url)
			html = response.read()
			print "Page Fetched for "+response.geturl()
			response.close()
			self.__network_failures_retry__ = 0 # Everything went OK, setting variable for network failure to 0
			return html
		except urllib2.URLError, e:
			print e.reason
			self.__network_failures_retry__ = self.__network_failures_retry__ + 1
			if self.__network_failures_retry__ < MAX_NETWORK_FAILURE_TRIES:
				print "Error occured, retrying in "+self.__network_failures_retry__" s"
				time.sleep(self.__network_failures_retry__)
				self.fetch_html(url)
		else:
			pass
		finally:
			pass

	def get_parsed_page_for_url(self, url=""):
		html_page = self.fetch_html(url)
		parsed_page = BeautifulSoup(html_page, "lxml")
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

	def convert_price_to_float(self, str_price):
		return float(self.strip_string(str_price).replace(",",".").replace(u'\u20ac',""))

	def strip_string(self, str):
		return " ".join(str.split())