#!/usr/bin/python
# -*- coding: utf-8 -*-

import mechanize
from urllib import urlencode
import time

from apps.scrapers.base.basecrawler import BaseCrawler, Singleton

class MonoprixCrawler(BaseCrawler, Singleton):

	def __init__(self):
		super(MonoprixCrawler, self).__init__()
		BaseCrawler.MAX_NETWORK_FAILURE_TRIES = 20
		BaseCrawler.INTERVAL = 2
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
		url = form_data['form']['url']
		formdata = form_data['form']['data']['t:formdata']
		data = { 't:formdata': formdata, 'radiogroup': 'LAD'}
		new_data = urlencode(data)

		request = mechanize.Request(url, new_data)
		request.add_header('Accept', 'text/javascript, text/html, application/xml, text/xml, */*')
		request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
		request.add_header('X-Requested-With', 'XMLHttpRequest')
		request.add_header('X-Prototype-Version', '1.7')
		html, code = self.do_request(request = request)

		return html, code


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
		data = { 'address': address}
		new_data = urlencode(data)
		request = mechanize.Request(url, new_data)
		request.add_header('Accept', 'text/javascript, text/html, application/xml, text/xml, */*')
		request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
		request.add_header('X-Requested-With', 'XMLHttpRequest')
		request.add_header('X-Prototype-Version', '1.7')
		html, code = self.do_request(request = request)

		return html, code
			


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
		url = address['url']
		request = mechanize.Request(url, '')
		request.add_header('Accept', 'text/javascript, text/html, application/xml, text/xml, */*')
		request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
		request.add_header('X-Requested-With', 'XMLHttpRequest')
		request.add_header('X-Prototype-Version', '1.7')
		html, code = self.do_request(request = request)

		return html, code

	def encodeTapestry(self, b):
		"""
			Encoding string tapestry style
		"""
		if b is None or len(b) == 0:
			return "$B"

		VALID_T5_CHARS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "_", ".", ":"]

		a = ""
		for i in xrange(0, len(b)):
			d = b[i]
			if d in VALID_T5_CHARS:
				a = a + d
			else:
				a = a +'%2400'+str.lstrip(hex(ord(b[i])), '0x') 
				# a = a +str.lstrip(hex(ord(b[i])), '0x') 
		return a

	def login_user(self, user_email = 'ahmed.boussadia@hotmail.fr', password = '2asefthukom,3'):
		"""
			This method authenticates and logs in user into oohop website
		"""
		# First get cookies by going to home page
		self.get('http://courses.monoprix.fr/');
		
		# Building url
		now = int(time.time())
		params = {'d': str(now)}
		url_params = urlencode(params)

		user_email = self.encodeTapestry((user_email))
		password = self.encodeTapestry((password))
		
		url_main = 'http://courses.monoprix.fr/action/IdentificationPage/'
		url_user = (user_email)+'/'+(password)+'/N/N'
		url = url_main+url_user+'?'+url_params

		return self.get(url)

	def empty_cart(self):
		"""
		"""

		url = 'http://courses.monoprix.fr/product.displaybasketright:removebasketevent/ShoppingCart'
		request = mechanize.Request(url, '')
		request.add_header('Accept', 'text/javascript, text/html, application/xml, text/xml, */*')
		request.add_header('Accept-Encoding', 'gzip,deflate,sdch')
		request.add_header('Accept-Language', 'en-US,en;q=0.8')
		request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
		request.add_header('X-Requested-With', 'XMLHttpRequest')
		request.add_header('X-Prototype-Version', '1.7')
		html, code = self.do_request(request = request)

		return html, code