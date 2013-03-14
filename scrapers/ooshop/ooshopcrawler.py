#!/usr/bin/python
# -*- coding: utf-8 -*-

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
