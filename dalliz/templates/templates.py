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

class Category(pystache.View):
	def set_products(self, products):
		self.__products = products
	
	def products(self):
		return self.__products

	def set_brands(self, brands):
		self.__brands = brands
	
	def brands(self):
		return self.__brands