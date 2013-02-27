#!/usr/bin/python
# -*- coding: utf-8 -*-

import mechanize
from urllib import urlencode

from scrapers.base.basecrawler import BaseCrawler


class AuchanCrawler(BaseCrawler):
	
	def __init__(self):
		BaseCrawler.MAX_NETWORK_FAILURE_TRIES = 20
		super(AuchanCrawler, self).__init__()

	def category_tag(self, tag):
		"""
			Filter category page by tag

			Input :
				- tag (hash) :
					{
						'name':...,
						'url': ...
					}

			Output :
				- html
				- code
		"""
		url = tag['url']
		data = {}
		new_data = urlencode(data)

		request = mechanize.Request(url, new_data)
		request.add_header('Accept', 'text/javascript, text/html, application/xml, text/xml, */*')
		request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
		request.add_header('X-Requested-With', 'XMLHttpRequest')
		request.add_header('X-Prototype-Version', '1.6.0.3')
		html, code = self.do_request(request = request)
		
		return html, code


