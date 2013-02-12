#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import simplejson as json
from urlparse import urlparse, parse_qs

from bs4 import BeautifulSoup

from scrapers.base.baseparser import BaseParser

class AuchanParser(BaseParser):

	def __init__(self, html = ''):
		super(AuchanParser, self).__init__(html)


	#-----------------------------------------------------------------------------------------------------------------------
	#
	#									INHERITED METHODS FROM BASE PARSER
	#
	#-----------------------------------------------------------------------------------------------------------------------

	def get_categories(self):
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
		categories = []
		# Getting menu
		menu = self.parsed_page.find(id="menu-principal")
		
		# Getting main categories
		for li in menu.findChildren('li', recursive = False):
			a = li.findChildren('a', recursive = False)[0]
			# Excluding last element, it is not a category
			if 'rel' not in a.attrs:
				a_html = unicode(a).replace('<br />', ' ').replace('<br/>', ' ')
				new_a = BeautifulSoup(a_html, "lxml", from_encoding = 'utf-8')
				main_category = {
					'name': new_a.text,
					'url': None,
					'sub_categories': []
					}

				# Now getting sub categories level 1
				div = li.findChildren('div', recursive = False)[0]
				for li_level_1 in div.find('ul').findChildren('li', recursive = False):
					category_level_1 = {
						'name': li_level_1.find('h3').find('a').text,
						'url': li_level_1.find('h3').find('a').attrs['href'],
						'sub_categories': []
					}

					# Now getting sub categories level 2
					as_level_2 = li_level_1.find_all('a')
					for a_level_2 in as_level_2:
						category_level_2 = {
							'name': a_level_2.text,
							'url': a_level_2.attrs['href']
						}
						category_level_1['sub_categories'].append(category_level_2)

					main_category['sub_categories'].append(category_level_1)

				categories.append(main_category)

		return categories

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
	#									SPECIFIC METHODS
	#
	#-----------------------------------------------------------------------------------------------------------------------

	def get_form_postal_code(self):
		"""
			Get form data in order to set location.

			Output :
				- form_data : {
					'url': ...,
					'data':{'name':value}
				}
		"""
		form_data = {'url':'','data':{}}
		parsed_page = self.parsed_page

		form = parsed_page.find('form', {'class': 'form-choose-postal'})
		if form:
			form_data['url'] = form.attrs['action']
			for input in form.find_all('input'):
				name = None
				value = None
				if 'name' in input.attrs:
					name = input.attrs['name']
				if 'value' in input.attrs:
					value = input.attrs['value']
				if name:
					form_data['data'][name] = value

		return form_data

