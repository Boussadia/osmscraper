#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from scrapers.base.baseparser import BaseParser

class OoshopParser(BaseParser):
	"""
		Ooshop parser

	"""

	def __init__(self, html = ''):
		super(OoshopParser, self).__init__(html)

	def get_categories(self, level = 0):
		"""
			Extract categories from html.

			Input :
				- level (int) : level of categories to extract. 0 = main catgories, 1 = sub categories level 1 ...
			Output :
				- categories : list hash represnting categories, example :
					[{
						'name':category_name,
					 	'url': url_category,
					 	'sub_categories':[...]
					 }]
		"""
		categories = []
		if level == 0:
			# Getting main categories
			a_main_menu = self.parsed_page.find_all("a",{"class":re.compile("univ(\d){1}")})
			li_sub = self.parsed_page.find(id="navh").find_all("li")
			print "Main menu contains %d categories."%(len(a_main_menu))

			for i in xrange(0,len(li_sub)):
				li = li_sub[i]
				a_main_cats = li.find_all("a",{"class":re.compile("univ(\d){1}")})
				if len(a_main_cats)>0:
					a = a_main_cats[0]
					name = a.find(text=True)
					url = a.get("href")
					category = {
						'name': name,
						'url':url,
						'sub_categories':[]
					}

					# Getting sub categories level 1
					sub_cats = li.find("div").find_all("a")

					print "Found %d sub categories for main category %s"%(len(sub_cats), name)

					sub_categories = []
					
					for j in xrange(0, len(sub_cats)):
						print "Found category %s"%(sub_cats[j].findAll(text=True)[0][2:])
						sub_categories.append( {
							"name": sub_cats[j].findAll(text=True)[0][2:],
							"url" : sub_cats[j].get("href"),
							'sub_categories':[]
						})
					category["sub_categories"] = sub_categories
					categories.append(category)

		elif level == 2:
			lis = self.parsed_page.find(id = "ctl00_cphC_ns_rpFilTab_ctl01_ucBns_p1" ).find_all("li")

			print "Found %d sub categories level 2 "%(len(lis))

			for i in xrange(0, len(lis)):
				li = lis[i]
				name_sub_category_level_2 = li.find("a").find(text=True)
				url_sub_category_level_2 = li.find("a").get("href")
				sub_categories_level_2 = {
					"name": name_sub_category_level_2,
					"url": url_sub_category_level_2,
					"sub_categories":[],
				}
				categories.append(sub_categories_level_2)
		elif level == 3:
			div = self.parsed_page.find(id="ctl00_cphC_ns_rpFilTab_ctl02_ucBns_p1")
			if div is not None:
				lis = div.find_all("li")
				print "Found %d sub categories level 3"%(len(lis))

				for i in xrange(0, len(lis)):
					li = lis[i]
					name_sub_category_level_3 = li.find("a").find(text=True)
					url_sub_category_level_3 = li.find("a").get("href")
					sub_categories_level_3 = {
						'name': name_sub_category_level_3,
						"url": url_sub_category_level_3,
					}
					categories.append(sub_categories_level_3)

		return categories

	def get_eligibility(self):
		"""
			Method responsible for parsing the eligibility page. When asking Ooshop if an area is eligible 
			for the service

			Output : 
				- boolean : whether the area is eligible or not
		"""
		el = self.parsed_page.find_all("div",{"class":"Elig"})
		return len(el)>0

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

	def parse_promotion_full(self):
		"""
			This method extracts information form a promtion page, it includes all informations relative
			to the promotion

			Return:
				ref. parse_promotion_short. And other inofmration depending on osm
		"""
		pass

	def get_form_values(self):
		"""
			Ooshop website is a .NET application that worls with a global form that encapsulates the body content.
			This method return a hash of name and values of the form.

			Output : 
				- hash : {'name': value}
		"""

		form_parsed = self.parsed_page.find(id='aspnetForm')
		inputs = form_parsed.find_all('input')
		form_data = {}
		for i in inputs:
			if 'name' in i.attrs:
				form_data[i.attrs['name']] = ''
				if 'value' in i.attrs:
					form_data[i.attrs['name']] = i.attrs['value']

		return form_data
