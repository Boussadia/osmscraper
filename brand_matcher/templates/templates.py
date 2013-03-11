#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pystache

class Osm_brand_matcher_pystache_view(pystache.View):
	def __init__(self):
		super(Osm_brand_matcher_pystache_view, self).__init__()
		self.template_path = os.path.abspath(os.path.dirname(__file__))
		self.template_encoding = 'utf-8'

class Brand_selector(Osm_brand_matcher_pystache_view):
	def set_osm_brand(self, osm_brand):
		self.__osm_brand = osm_brand

	def osm_brand(self):
		return self.__osm_brand

	def set_dalliz_brands(self, brands):
		self.__dalliz_brands = brands

	def dalliz_brands(self):
		return self.__dalliz_brands