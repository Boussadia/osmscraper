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
		html, code, cookie = self.fetch_html_cookie(url)
		return html, code

	def fetch_html_cookie(self, url="", cookie = None):
		try:
			url = self.pre_processing_url(url)
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
			request = urllib2.Request(url)
			if cookie is not None:
				request.add_header('cookie', cookie)
			response = urllib2.urlopen(request)
			response_cookie = response.headers.get('Set-Cookie')
			html = response.read()
			print "Page Fetched for "+response.geturl()
			response.close()
			self.__network_failures_retry__ = 0 # Everything went OK, setting variable for network failure to 0
			return html, 200, response_cookie
		except urllib2.HTTPError, e:
			if e.code == 404:
				print "Error when retrieving "+url+" : page not found."
				return None, 404, None
			else:
				self.__network_failures_retry__ = self.__network_failures_retry__ + 1
				if self.__network_failures_retry__ < OSMScraper.MAX_NETWORK_FAILURE_TRIES:
					print "Error occured, retrying in "+str(self.__network_failures_retry__)+" s"
					time.sleep(self.__network_failures_retry__)
					return self.fetch_html(url)
				else:
					print "Error when retrieving "+url
					return None, e.code, None
		except urllib2.URLError, e:
			self.__network_failures_retry__ = self.__network_failures_retry__ + 1
			if self.__network_failures_retry__ < OSMScraper.MAX_NETWORK_FAILURE_TRIES:
				print "Error occured, retrying in "+str(self.__network_failures_retry__)+" s"
				time.sleep(self.__network_failures_retry__)
				return self.fetch_html(url)
			else:
				print "Error when retrieving "+url
				return None, -1, None

	def get_parsed_page_for_url(self, url=""):
		parsed_page, code, cookie = self.get_parsed_page_for_url_cookie(url)
		return parsed_page, code

	def get_parsed_page_for_url_cookie(self, url="", cookie = None):
		html_page, code, cookie = self.fetch_html_cookie(url, cookie)
		if html_page is not None:
			parsed_page = BeautifulSoup(html_page, "lxml", from_encoding = 'utf-8')
		else:
			parsed_page = BeautifulSoup("", "lxml", from_encoding = 'utf-8')
		return parsed_page, code, cookie

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

	def pre_processing_url(self, url):
		return url