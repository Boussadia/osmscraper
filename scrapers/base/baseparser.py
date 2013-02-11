#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup

class BaseParser(object):
	"""
		Base Parser class for online supermarket sites. This class has to be inherited to implement specif methods.

		This class provides the following methods :
			- get_categories : retrieves categories
			- get_products : retrives products from a category page (without complete description)
			- get_product_info : retrieves all product information form a product page
	"""

	def __init__(self, html):
		"""
			Input :
				- html (string) : string containing the html code of a page.
		"""
		self.parsed_page = BeautifulSoup(html, "lxml", from_encoding = 'utf-8')


	#-----------------------------------------------------------------------------------------------------------------------
	#
	#									METHODS TO BE DEFINED IN INHERITED CLASSES
	#
	#-----------------------------------------------------------------------------------------------------------------------

	def get_categories(self, level = 0, depth = 1 ):
		"""
			Extract categories from html.

			Input :
				- level (int) : level of categories to extract. 0 = main catgories, 1 = sub categories level 1 ...
				- depth (int) : how many levels of categories to extract. -1 = all sub levels.
			Output :
				- categories : list hash represnting categories, example :
					[{
						'name':category_name,
					 	'url': url_category,
					 	'sub_categories':[...]
					 }]
		"""
		pass

	def get_products(self):
		"""
			Extracts products from a category page.

			Output :
				- products : list of hash representing products, example:
					[{
						'reference': 23435906324,
						'name': product_name,
						'url': product_url,
						'package' : '3 bouteilles de 100 ml',
						'price': 2.3,
						'unit': 'ml',
						'unit_price': 5,
						'brand': brand_name # optionnal, depends on osm
						'available': True
						'is_promotion' : True,
						'promotion':{
							# Content specific to promotion and osm, ref. method parse_promotion_short
						}
					}]
		"""
		pass

	def parse_promotion_short(self):
		"""
			This method is responsible for extracting information regarding promotion in a product form a category page.

			Output : 
				- hash representing promotion of product. Example
					- for simple promotion :
						{
							'type': 'simple',
							'normal_price': 3,
							'new_unit_price': 4,
							'promotion_price': 2,
							'beginnig_date': 'dd-mm-YYYY',
							'end_date': 'dd-mm-YYYY',
						}
					- for multi promotion (more than 1 product offer):
						{
							'type': 'multi',
							'normal_price': 3,
							'new_unit_price': 4,
							'promotion_price': 2,
							'beginnig_date': 'dd-mm-YYYY',
							'end_date': 'dd-mm-YYYY',
						}	

		"""
		pass

	def parse_product_full(self):
		"""
			This method is responsible for extracting information from a product page.
			It behaves the same as get_products for a single product and also returns detailed information about the product.
		"""

	def parse_promotion_full(self):
		"""
			This method extracts information form a promtion page, it includes all informations relative
			to the promotion

			Return:
				ref. parse_promotion_short. And other inofmration depending on osm
		"""
		pass

	def extract_package_content(self, package):
		"""
			This method extracts package content of a product.
			e.g. '4 pots de yaourt de 200g' -> {'quantity': 4, 'unit_quantity': 200, 'unit': g}

			Input :
				- package (string) : description of the content of a product
			Output : 
				- hash describing content
		"""


	#-----------------------------------------------------------------------------------------------------------------------
	#
	#									COMMON METHODS
	#
	#-----------------------------------------------------------------------------------------------------------------------

	def convert_to_float(self, price):
		"""
			Take a price and converts it to a float

			Input :
				- price (string) : e.g. '2,30 €'
			Output :
				- price (float) : e.g. 2.3
		"""
		return float(self.strip_string(price).replace(",",".").replace(u'\u20ac',""))

	def strip_string(self, str):
		"""
			Cleaning string.
		"""
		return " ".join(str.split())

	def set_html(self, html):
		self.parsed_page = BeautifulSoup(html, "lxml", from_encoding = 'utf-8')

	def properurl(self, url_to_format):
		"""
			Formating a proper url :
				base_url = 'http://www.example.com', url_to_format = 'path/to/page' -> 'http://www.example.com/path/to/page'
				base_url = 'http://www.example.com', url_to_format = 'http://www.example.com/path/to/page' -> 'http://www.example.com/path/to/page'
		"""
		base_url = self.base_url
		scheme_base, netloc_base, path_base, params_base, query_base, fragment_base = urlparse(base_url)
		scheme, netloc, path, params, query, fragment = urlparse(url_to_format)

		return urlunparse((scheme_base, netloc_base, path, params, query, fragment))

	def extract_package_content(self, str_package):
		"""
			This method extracts package content of a product.
			e.g. '4 pots de yaourt de 200g' -> {'quantity': 4, 'quantity_measure': 200, 'unit': g}

			Input :
				- str_package (string) : description of the content of a product
			Output : 
				- hash describing content
		"""
		package = {}
		regexp1 = r'(\d+)x(\d+,?\d*) ?([^\W\d_]+)' # type = 6x33cl
		regexp2 = r'(\d+)(?!,)[^\d]+(\d+,?\d*) ?([^\W\d_]+)' # type = les 3 boites de 200g
		regexp3 = r'[\w\D]+(\d+)\D+(\d+,?\d*) ?([^\W\d_]+)' # la barquette de 2, 350g
		regexp4 = r'(\d+,?\d*) ?([^\W\d_]+)' # type = La bouteille de 1,5L
		m = re.search(regexp1, str_package)
		if m:
			# found first type package content
			package = {
				'quantity': m.group(1),
				'quantity_measure': self.convert_to_float(m.group(2)),
				'unit': m.group(3)
			}
		else:
			m = re.search(regexp2, str_package)
			if m:
				# type 2 content
				package = {
					'quantity': m.group(1),
					'quantity_measure': self.convert_to_float(m.group(2)),
					'unit': m.group(3)
				}
			else:
				m = re.search(regexp3, str_package)
				if m:
					# type 3 content
					package = {
						'quantity': m.group(1),
						'quantity_measure': self.convert_to_float(m.group(2)),
						'unit': m.group(3)
					}
					
				else:
					m = re.search(regexp4, str_package)
					if m:
						# type 4 content
						package = {
							'quantity': 1,
							'quantity_measure': self.convert_to_float(m.group(1)),
							'unit': m.group(2)
						}

		package.update({'str': str_package})
		return package
