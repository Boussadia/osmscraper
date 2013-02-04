#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import urllib
import urllib2
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
		# Initialising cookie jar & opener
		self.jar = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.jar))
		self.__network_failures_retry__ = 0 # 

	def do_request(self, url, data = {}):
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
			print "Fetching page from "+url
			if data == {}:
				print "GET method used"
				response = self.opener.open(url)
				html = response.read()
			else:
				print "POST method used"
				form_data = urllib.urlencode(data)
				response = self.opener.open(url, form_data)
				html = response.read()

			self.__network_failures_retry__ = 0 # Everything went OK, setting variable for network failure to 0
			return html, 200

		except urllib2.HTTPError, e:
			if e.code == 404:
				print "Error when retrieving "+url+" : page not found."
				return None, 404
			else:
				self.__network_failures_retry__ = self.__network_failures_retry__ + 1
				if self.__network_failures_retry__ < Crawler.MAX_NETWORK_FAILURE_TRIES:
					print "Error occured, retrying in "+str(self.__network_failures_retry__)+" s"
					time.sleep(self.__network_failures_retry__)
					return self.do_request(url, data)
				else:
					print "Error when retrieving "+url
					return None, e.code
		except urllib2.URLError, e:
			self.__network_failures_retry__ = self.__network_failures_retry__ + 1
			if self.__network_failures_retry__ < Crawler.MAX_NETWORK_FAILURE_TRIES:
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

	def post(url, data):
		"""
			Executes a POST url fetch.
		"""
		return self.do_request(url, data)


