#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pystache

class Ooshop_brand_matcher_pystache_view(pystache.View):
	def __init__(self):
		super(Ooshop_brand_matcher_pystache_view, self).__init__()
		self.template_path = os.path.abspath(os.path.dirname(__file__))
		self.template_encoding = 'utf-8'

class Brand_selector(Ooshop_brand_matcher_pystache_view):
	def set_ooshop_brand(self, ooshop_brand):
		self.__ooshop_brand = ooshop_brand

	def ooshop_brand(self):
		return self.__ooshop_brand

	def set_dalliz_brands(self, brands):
		self.__dalliz_brands = brands

	def dalliz_brands(self):
		return self.__dalliz_brands