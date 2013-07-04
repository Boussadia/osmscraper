#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import urllib
import mechanize
import cookielib
import sys
import urlparse

class Singleton(object):
  _instances = {}
  def __new__(class_, *args, **kwargs):
    if class_ not in class_._instances:
        class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
    return class_._instances[class_]


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
	INTERVAL = 0 # interval between 2 http request in seconds

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

		# time of last http request
		self.last_time = time.time() - BaseCrawler.INTERVAL

	def do_request(self, url ='', data = {}, request = None, is_post = False, url_fix = True):
		"""
			Base method to perform a request to a url.

			Input :
				- url (string) : url of page to retrive
				- data (hash {'param': 'value_param'}) : data to send to server, if an empty hash, it is not taken into account

			Output:
				- (html, code) : html as string and code as defined in the class docstring.
		"""
		if url_fix:
			# Making sure it is utf8 encoded
			url = self.url_fix(url)
		# Request cannot happen inside a cetain lapse of time (INTERVAL seconds in between)
		now = time.time()
		if now-self.last_time<BaseCrawler.INTERVAL:
			print 'Waiting %d ms in order not to flood server'%((BaseCrawler.INTERVAL+self.last_time-now)*1000)
			time.sleep(BaseCrawler.INTERVAL+self.last_time-now)
			return self.do_request( url, data, request, is_post= is_post, url_fix = url_fix)
		self.last_time = now

		# Encapsulating request in try block in order to catch HTTPError 
		try:
			if request is not None:
				self.jar.add_cookie_header(request)
				response = self.browser.open(request)
				print "Fetching page from "+response.geturl()
				print "Using personalized Request"
				html = response.read()
			elif not is_post:
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
					return self.do_request(url, data, is_post = is_post, url_fix = url_fix)
				else:
					print "Error when retrieving "+url
					return None, e.code
		except mechanize.URLError, e:
			print 'Error : %s'%(e)
			self.__network_failures_retry__ = self.__network_failures_retry__ + 1
			if self.__network_failures_retry__ < BaseCrawler.MAX_NETWORK_FAILURE_TRIES:
				print "Error occured, retrying in "+str(self.__network_failures_retry__)+" s"
				time.sleep(self.__network_failures_retry__)
				return self.do_request(url, data, is_post = is_post, url_fix = url_fix)
			else:
				print "Error when retrieving "+url
				return None, -1
		except Exception, e:
			print 'Unexpected error occured.'
			print e
			return None, -1

	def get(self,url, url_fix = True):
		"""
			Executes a GET url fetch.
		"""
		return self.do_request(url, url_fix = url_fix)

	def post(self, url, data = {}, url_fix = True):
		"""
			Executes a POST url fetch.
		"""
		return self.do_request(url, data = data, is_post=True, url_fix = url_fix)

	def empty_cookie_jar(self):
		"""
			Removing all cookies from cookie jar
		"""
		self.jar.clear()

	def get_cookie(self, name = None):
		"""
			Get cookie by name
			Input : 
				- name (string) : name of cookie.
			Output :
				- hash : {
					'name': ...,
					'value': ...
				}
		"""

		cookie = {}

		if name:
			for c in self.jar:
				if name == c.name:
					cookie['name'] = c.name
					cookie['value'] = c.value
					
		return cookie

	def url_fix(self, s, charset='utf-8'):
		"""
			Sometimes you get an URL by a user that just isn't a real
			URL because it contains unsafe characters like ' ' and so on.  This
			function can fix some of the problems in a similar way browsers
			handle data entered by the user:

			>>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklärung)')
			'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

			:param charset: The target charset for the URL if the url was
			given as unicode string.
		"""
		if isinstance(s, unicode):
			s = s.encode(charset, 'ignore')
		scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
		path = urllib.quote(path, '/%')
		qs = urllib.quote_plus(qs, ':&=')
		return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))



