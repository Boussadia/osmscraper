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

	#-----------------------------------------------------------------------------------------------------------------------
	#
	#									INHERITED METHODS FROM BASE PARSER
	#
	#-----------------------------------------------------------------------------------------------------------------------

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
		promotion = {}
		promotion_html = self.parsed_page.find(id='ctl00_ucDetProd_upProd')

		# Getting price before and after promotion
		price_block = promotion_html.find('p', {'class' : 'strikePrice'})
		price_after = self.convert_to_float(price_block.find('strong').find(text=True))
		price_before = self.convert_to_float(price_block.find('strike').find(text=True))
		promotion['before'] = price_before
		promotion['after'] = price_after

		# After price_block, ooshop indicates dates of promotion
		date_block = price_block.nextSibling
		results = re.findall(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_block.find(text=True))
		promotion.update(dict(zip(['date_start', 'date_end'], [ dict(zip(['day','month', 'year'], r)) for r in results])))

		# Getting package content unit price and unit - determining type of promotion
		promotion_info_ps = price_block.parent()
		for p in promotion_info_ps:
			text = p.find(text=True)
			# Appyling reg
			match = re.search(r'(\d+),?(\d*) ?\W ?/ ?(\w{1,5})', text)
			if match:
				# Unit price and unit
				unit_price = float('%s.%s'%(match.group(1), match.group(2)))
				unit = match.group(3)
				promotion['unit_price'] = unit_price
				promotion['unit'] = unit
				
				if 'lot' in promotion['unit'].lower():
					# Multiple promotion
					promotion['type'] = 'multi'

					# Extracting image url of products in promotion (url of product not available in this section...)
					content_promotion = self.parsed_page.find(id='ctl00_cphC_pn3T1_ctl01_pDetLot')
					products_lot = content_promotion.find_all(id=re.compile('ctl00_cphC_pn3T1_ctl01_rptDetailLot_ctl(\d{2})_plProd_divPnl'))
					promotion['product_image_urls'] = [p.find('a').find('img').attrs['src'] for p in products_lot]


				else:
					# Multiple promotion
					promotion['type'] = 'simple'


		

		return promotion
		

	def parse_product_full(self):
		"""
			This method is responsible for extracting information from a product page.
			It behaves the same as get_products for a single product and also returns detailed information about the product.
		"""
		# Initializing product hash
		product = {
			'is_product': False,
			'is_promotion': False,
			'is_available': False
		}
		# encapsulatating in try except block

		product_html = self.parsed_page.find(id='ctl00_ucDetProd_upProd')
		product['html'] = product_html.prettify()

		if product_html:
			# Common to promotion and normal product
			# Is the product available ?
			img_unavailable = self.parsed_page.find(id='ctl00_cphC_pn3T1_ctl01_imgOther')
			print img_unavailable
			if img_unavailable:
				product['is_available'] = False
			else:
				product['is_available'] = True

			# Extracting product name and brand
			name_and_brand = product_html.find('h3', {'class', 'BmarginSm'}).find(text=True)
			# Cleaning from spaces and carriage return
			name_and_brand = re.search('(\\n| |\\r\\n)+(.*)(\\n| |\\r\\n)*', name_and_brand).group(2)
			# Seperating name and brand
			name_and_brand = name_and_brand.split(' - ')
			product['name'] = ' - '.join(name_and_brand[:-1])
			product['brand'] = name_and_brand[-1:][0]

			# Getting images
			product_image = self.parsed_page.find(id='ctl00_cphC_pn3T1_ctl01_imgVisu')
			product_image_url = product_image.attrs['src']
			brand_image = self.parsed_page.find(id='ctl00_cphC_pn3T1_ctl01_iLogo')
			brand_image_url = brand_image.attrs['src']
			product['product_image_url'] = product_image_url
			product['brand_image_url'] = brand_image_url

			# Checking if promotion
			promotion_html = product_html.find('a', {'class': 'btnRectSimple'})
			if promotion_html:
				# This product is a promotion
				product['is_promotion'] = True
				product['promotion'] = self.parse_promotion_full()
			
			else:
				# This is a normal product
				product['is_product'] = True

				# Getting base product information
				product_info = self.parsed_page.find(id='ctl00_cphC_pn3T1_ctl01_divContentPromNouv')

				# Getting price
				price = product_info.find('p', {'class', 'price'}).find('strong').find(text= True)
				product['price'] = self.convert_to_float(price)

				# Getting package content unit price and unit
				product_info_ps = product_info.find_all('p')
				for p in product_info_ps:
					if 'class' not in p.attrs:
						text = p.find(text=True)
						# Appyling reg
						match = re.search(r'(\d+),?(\d*) ?\W ?/ ?(\w{1,5})', text)
						if match:
							# Unit price and unit
							unit_price = float('%s.%s'%(match.group(1), match.group(2)))
							unit = match.group(3)
							product['unit_price'] = unit_price
							product['unit'] = unit
							# Package
							package = self.extract_package_content(p.previous_sibling.find(text=True))
							product['package'] = package
							

				# Extracting detailed information about the product
				information = {}
				# Is there an origin for this product ?
				origin_parsed = self.parsed_page.find(id='ctl00_cphC_pn3T1_ctl01_lOrigine')
				if origin_parsed:
					information['origin'] = self.strip_string(origin_parsed.find('span',{'class' : 'origine'}).find(text=True))
				# First : nutritional information
				nutritional_info = self.parsed_page.find(id='ctl00_cphC_pn3T1_ctl01_pIg')
				if nutritional_info:
					# Information found
					title_info = self.parsed_page.find(id='ctl00_cphC_pn3T1_ctl01_lTig').find(text=True)
					tds = self.parsed_page.find(id='ctl00_cphC_pn3T1_ctl01_lHig').find_all('td')
					information[title_info] = dict([[self.strip_string(string) for string in td.findAll(text=True) if self.strip_string(string) != ''] for td in tds])

				# Then all the other information
				information_titles_html = self.parsed_page.find_all(id = re.compile(r'ctl00_cphC_pn3T1_ctl01_lTitre\d'))
				information_titles = [' '.join(html.find_all(text=True)) for html in information_titles_html]
				information_content_html = self.parsed_page.find_all(id = re.compile(r'ctl00_cphC_pn3T1_ctl01_lHtml\d'))
				information_content = [' '.join(html.find_all(text=True)) for html in information_content_html]

				information.update(dict(zip(information_titles, information_content)))

				product['information'] = information

		else:
			product['is_product'] = False
			
		return product

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
		regexp1 = r'(\d+)x(\d+,?\d*) ?(\w+)' # type = 6x33cl
		regexp2 = r'(\d+)[^\d]+(\d+,?\d*) ?(\w+)' # type = les 3 boites de 200g
		regexp3 = r'(\d+,?\d*) ?(\w+)' # type = La bouteille de 1,5L
		m = re.search(regexp1, str_package)
		if m:
			# found first type package content
			package = {
				'quantity': m.group(1),
				'quantity_measure': m.group(2),
				'unit': m.group(3)
			}
		else:
			m = re.search(regexp2, str_package)
			if m:
				# type 2 content
				package = {
					'quantity': m.group(1),
					'quantity_measure': m.group(2),
					'unit': m.group(3)
				}
			else:
				m = re.search(regexp3, str_package)
				if m:
					# type 3 content
					package = {
						'quantity': 1,
						'quantity_measure': m.group(1),
						'unit': m.group(2)
					}

		package.update({'str': str_package})
		return package

	#-----------------------------------------------------------------------------------------------------------------------
	#
	#									SPECIFIC METHODS TO OOSHOP PARSER
	#
	#-----------------------------------------------------------------------------------------------------------------------

	def get_form_values(self):
		"""
			Ooshop website is a .NET application that works with a global form that encapsulates the body content.
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
