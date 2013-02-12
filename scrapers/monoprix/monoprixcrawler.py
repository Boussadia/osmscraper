#!/usr/bin/python
# -*- coding: utf-8 -*-

import mechanize
from urllib import urlencode

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

	def set_delivery(self,form_data):
		"""
			Setting the delivery

			Input : 
				form_data :
					{
						'type': 'select' or 'address',
						'form': {
							'url' : rul of form
							'data' : {data to pass to requery}
						}
					}
		"""
		try:
			url = form_data['form']['url']
			formdata = form_data['form']['data']['t:formdata']
			data = { 't:formdata': formdata, 'radiogroup': 'LAD'}
			new_data = urlencode(data)
			print "Fetching page from "+url
			print "POST method used"

			request = mechanize.Request(url, new_data)
			request.add_header('Accept', 'text/javascript, text/html, application/xml, text/xml, */*')
			request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
			request.add_header('X-Requested-With', 'XMLHttpRequest')
			request.add_header('X-Prototype-Version', '1.7')
			self.jar.add_cookie_header(request)
			response = self.browser.open(request)
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

	def search_adress(self, address):
		"""
			Searching for address in order to localize a user

			Input :
				- address (string) : '(address), (postal code) (city)'
			Output :
				- html
				- code
		"""
		url = 'http://courses.monoprix.fr/productlist.popupcontainer.popupident.popupidentaddress.qassearchaddress.addressqas:refreshqasresultzone'
		try:
			data = { 'address': address}
			new_data = urlencode(data)
			print "Fetching page from "+url
			print "POST method used"

			request = mechanize.Request(url, new_data)
			request.add_header('Accept', 'text/javascript, text/html, application/xml, text/xml, */*')
			request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
			request.add_header('X-Requested-With', 'XMLHttpRequest')
			request.add_header('X-Prototype-Version', '1.7')
			self.jar.add_cookie_header(request)
			response = self.browser.open(request)
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


	def set_address(self, address):
		"""
			Setting address in order to localize a user

			Input :
				- address :{
					'url': /path/to/address/validation
				}
			Output :
				- html
				- code
		"""
		try:
			url = address['url']
			print "Fetching page from "+url
			print "POST method used"

			request = mechanize.Request(url, '')
			request.add_header('Accept', 'text/javascript, text/html, application/xml, text/xml, */*')
			request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
			request.add_header('X-Requested-With', 'XMLHttpRequest')
			request.add_header('X-Prototype-Version', '1.7')
			self.jar.add_cookie_header(request)
			response = self.browser.open(request)
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