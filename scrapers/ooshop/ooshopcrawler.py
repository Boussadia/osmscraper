#!/usr/bin/python
# -*- coding: utf-8 -*-

import mechanize
from urllib import urlencode

from scrapers.base.basecrawler import BaseCrawler, Singleton

class OoshopCrawler(BaseCrawler, Singleton):

	def __init__(self):
		super(OoshopCrawler, self).__init__()

	def category_pagination(self, url, pagination):
		"""
			This method is the equivalent of clicking on a number of the pagination in order to get an other page of a category page.

			Input :
				- pagination (hash) : page information to fetch
			Output:
				- code : page retrieved from wed?
				- html : fetched html
		"""
		return self.__do_PostBack(url, pagination['eventTarget'], pagination['eventArgument'],'ctl00$cphC$pn3T1$ctl01$upPaginationH')

	def __do_PostBack(self, url, eventTarget, eventArgument, ctrl, options = None):
		"""
			Method specific to ooshop in order to retrieve pagination data.
		"""
		values = {}

		values["__EVENTTARGET"] = eventTarget
		values["__EVENTARGUMENT"] = eventArgument
		values["__LASTFOCUS"] = ""
		values["ctl00$sm"] = ctrl+'|'+eventTarget

		if options is not None:
			values.update(options)

		return self.post(url, values)

	def brand_filter(self, url, brand):
		"""
			This method is the equivalent of filtering products by brand name in a category page

			Input :
				- brand_value (string) : brand value in option tag
			Output:
				- code : page retrieved from wed?
				- html : fetched html
		"""
		return self.__do_PostBack(url, eventTarget = brand['eventTarget'], eventArgument = '', ctrl = 'ctl00$cphC$pn3T1$upPN3T1', options = {brand['eventTarget']:brand['value'], 'ctl00$cphC$pn3T1$ctl01$ddlTri':'Aucun', '__VIEWSTATE': brand['__VIEWSTATE']})

	def login_user(self, url, data):
		"""
			This method authenticates and logs in user into oohop website
		"""
		new_data = urlencode(data)
		request = mechanize.Request(url, new_data)
		request.add_header('Accept', '*/*')
		request.add_header('Accept-Encoding', 'gzip,deflate,sdch')
		# request.add_header('X-MicrosoftAjax', 'Delta=true')
		request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
		request.add_header('Accept-Language', 'en-US,en;q=0.8')
		request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')
		request.add_header('Cache-Control', 'no-cache')
		request.add_header('Origin', 'http://www.ooshop.com')
		request.add_header('Referer', url)
		request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31')

		# request.add_header('X-Requested-With', 'XMLHttpRequest')
		# request.add_header('X-Prototype-Version', '1.7')
		return self.do_request(request = request)



