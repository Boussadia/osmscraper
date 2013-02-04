#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import re

class Parser(object):
	"""
		Base Parser class for online supermarket sites. This class has to be inherited to implement specif methods.

		This class provides the following methods :
			- get_categories : retrieves categories
			- get_products : retrives products from a category page (without complete description)
			- get_product_info : retrieves all product information form a product page
	"""

	def __init__(self):
		pass

	def get_categories(self, html, level = 0, depth = 1 ):
		"""
			Extract categories from html.

			Input :
				- html (string) : string containing the html code of a page.
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

	def get_products(self, html):
		"""
			Extracts products from a category page.

			Input :
				- html (string) : html of category page.
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

	def parse_promotion_short(self, html_product_short):
		"""
			This method is responsible for extracting information regarding promotion in a product form a category page.

			Input :
				- html_product_short (string) : html from a product element in a category page.

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

	def parse_promotion_full(self, html_product_full):
		"""
			This method extracts information form a promtion page, it includes all informations relative
			to the promotion

			Input : 
				- html_product_full (string) : html of a promotion page
			Return:
				ref. parse_promotion_short. And other inofmration depending on osm
		"""
		pass