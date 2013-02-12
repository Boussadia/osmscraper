#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import urllib
import mechanize
import cookielib


class BaseCrawler(object):
	"""
		Base Crawler class.
		
		The Crawler has to perform:
			- GET methods
			- POST methods
			- handle cookies

		In order to take into account for the network failures, it will handle a certain amount of retries.

		Every time a page is fetched, it has to return a code as well, he are the definition of the codes:
			- -1 : Network failure (after N number of attempts)
			- 200 : every thing is ok
			- 404 : page not found
			- 500 : server error

	"""

	# The number of times the crawler has to retry to fetch html page when a network failure error occurs
	MAX_NETWORK_FAILURE_TRIES = 10

	def __init__(self):
		# Mechanize Browser
		self.browser = mechanize.Browser()
		# Cookie Jar
		self.jar = cookielib.LWPCookieJar()
		self.browser.set_cookiejar(self.jar)
		# Browser options
		self.browser.set_handle_equiv(True)
		# self.browser.set_handle_gzip(True)
		self.browser.set_handle_redirect(True)
		self.browser.set_handle_referer(True)
		self.browser.set_handle_robots(False)

		# Follows refresh 0 but not hangs on refresh > 0
		self.browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

		self.__network_failures_retry__ = 0

	def do_request(self, url ='', data = {}, request = None):
		"""
			Base method to perform a request to a url.

			Input :
				- url (string) : url of page to retrive
				- data (hash {'param': 'value_param'}) : data to send to server, if an empty hash, it is not taken into account

			Output:
				- (html, code) : html as string and code as defined in the class docstring.
		"""
		# Encapsulating request in try block in order to catch HTTPError 
		try:
			if request is not None:
				self.jar.add_cookie_header(request)
				response = self.browser.open(request)
				print "Fetching page from "+response.geturl()
				print "Using personalized Request"
				html = response.read()
			elif data == {}:
				print "Fetching page from "+url
				print "GET method used"
				response = self.browser.open(url)
				html = response.read()
			else:
				print "Fetching page from "+url
				print "POST method used"
				form_data = urllib.urlencode(data)
				response = self.browser.open(url, form_data)
				html = response.read()

			self.__network_failures_retry__ = 0 # Everything went OK, setting variable for network failure to 0
			return html, 200

		except mechanize.HTTPError, e:
			if e.code == 404:
				print "Error when retrieving "+url+" : page not found."
				return None, 404
			else:
				print 'Error : %s'%(e)
				self.__network_failures_retry__ = self.__network_failures_retry__ + 1
				if self.__network_failures_retry__ < BaseCrawler.MAX_NETWORK_FAILURE_TRIES:
					print "Error occured, retrying in "+str(self.__network_failures_retry__)+" s"
					time.sleep(self.__network_failures_retry__)
					return self.do_request(url, data)
				else:
					print "Error when retrieving "+url
					return None, e.code
		except mechanize.URLError, e:
			print 'Error : %s'%(e)
			self.__network_failures_retry__ = self.__network_failures_retry__ + 1
			if self.__network_failures_retry__ < BaseCrawler.MAX_NETWORK_FAILURE_TRIES:
				print "Error occured, retrying in "+str(self.__network_failures_retry__)+" s"
				time.sleep(self.__network_failures_retry__)
				return self.do_request(url, data)
			else:
				print "Error when retrieving "+url
				return None, -1
		except Exception, e:
			print 'Unexpected error occured.'
			print e
			return None, -1

	def get(self,url):
		"""
			Executes a GET url fetch.
		"""
		return self.do_request(url)

	def post(self, url, data):
		"""
			Executes a POST url fetch.
		"""
		return self.do_request(url, data)

	def empty_cookie_jar(self):
		"""
			Removing all cookies from cookie jar
		"""
		self.jar.clear()



