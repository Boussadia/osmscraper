#!/usr/bin/python
# -*- coding: utf-8 -*-

from scrapers.base.basecrawler import BaseCrawler

class OoshopCrawler(BaseCrawler):

	def __init__(self):
		super(OoshopCrawler, self).__init__()

	def __do_PostBack(self, url, eventTarget, eventArgument):
		"""
			Method specific to ooshop in order to retrieve pagination data.
		"""
		values = {}

		values["__EVENTTARGET"] = eventTarget
		values["__EVENTARGUMENT"] = eventArgument
		values["__LASTFOCUS"] = ""
		values["ctl00$sm"] = 'ctl00$cphC$pn3T1$ctl01$upPaginationH|'+eventTarget

		return self.post(url, values)