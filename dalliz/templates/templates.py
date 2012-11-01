#!/usr/bin/python
# -*- coding: utf-8 -*-

import pystache
import os

pystache.View.template_path = os.path.abspath(os.path.dirname(__file__))
pystache.View.template_encoding = 'utf-8'

class Product(pystache.View):
	def set_product(self, product):
		self.__product = product
	
	def product(self):
		return self.__product
	