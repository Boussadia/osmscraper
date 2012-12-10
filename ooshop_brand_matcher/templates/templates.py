#!/usr/bin/python
# -*- coding: utf-8 -*-

import pystache
import os

class Brand_selector(pystache.View):
	def set_ooshop_brand(self, ooshop_brand):
		self.__ooshop_brand = ooshop_brand

	def ooshop_brand(self):
		return self.__ooshop_brand

	def set_dalliz_brands(self, brands):
		self.__dalliz_brands = brands

	def dalliz_brands(self):
		return self.__dalliz_brands