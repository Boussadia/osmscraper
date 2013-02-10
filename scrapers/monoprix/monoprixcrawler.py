#!/usr/bin/python
# -*- coding: utf-8 -*-

from scrapers.base.basecrawler import BaseCrawler

class MonoprixCrawler(BaseCrawler):

	def __init__(self):
		super(MonoprixCrawler, self).__init__()
		# Monoprix does mot like Python user agemt, so we are cheating a little bit ...
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; Intel Mac OS X 10.6; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'
		self.browser.addheaders = [('User-agent', user_agent)]		

	# def category_pagination(self, url, pagination):
	# 	"""
	# 		This method is the equivalent of clicking on a number of the pagination in order to get an other page of a category page.

	# 		Input :
	# 			- pagination (hash) : page information to fetch
	# 		Output:
	# 			- code : page retrieved from wed?
	# 			- html : fetched html
	# 	"""
	# 	return self.__do_PostBack(url, pagination['eventTarget'], pagination['eventArgument'])




	# def __do_PostBack(self, url, eventTarget, eventArgument):
	# 	"""
	# 		Method specific to ooshop in order to retrieve pagination data.
	# 	"""
	# 	values = {}

	# 	values["__EVENTTARGET"] = eventTarget
	# 	values["__EVENTARGUMENT"] = eventArgument
	# 	values["__LASTFOCUS"] = ""
	# 	values["ctl00$sm"] = 'ctl00$cphC$pn3T1$ctl01$upPaginationH|'+eventTarget

	# 	return self.post(url, values)