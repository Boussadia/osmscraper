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

	def set_html_from_tag(self, content):
		"""
			When filtering by tag, the crawler receives a json object with html inside it.

			Input :
				- content : {
					"content":...,
					"script":...,
					"zones":{
						"productListZone":...,
						"moreProductListZone":...,
						"labelZone":...
					}
				}
		"""
		content = json.loads(content)
		html = content['zones']['productListZone']

		self.set_html(html)

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
		parsed_page = self.parsed_page
		products = []

		for bloc_product in parsed_page.find_all('div',{'class': 'bloc-produit'}):
			product = {
				'from': 'category_page',
				'is_promotion': False,
				'is_product': False,
				'is_available': False,
			}
			bloc_product_classes =  bloc_product.attrs['class']
			
			if 'promotion' in bloc_product_classes:
				product['is_promotion'] = True
			else:
				product['is_product'] = True

			if 'bientot-dispo' not in bloc_product_classes:
				product['is_available'] = True

			# Common to promotion and product:
			url = bloc_product.find('a').attrs['href']
			product_image_url = bloc_product.find('a').find('img').attrs['src'].replace('line', 'detail')
			reference = url.split('/')[-1].split(';jsessionid=')[0]
			# Brands are either in h3 or h2 tags
			brand_block = bloc_product.find('div',{'class':'infos-produit-2'})
			if brand_block.find('h2'):
				brand = brand_block.find('h2').text
			elif brand_block.find('h3'):
				brand = brand_block.find('h3').text

			name = " ".join([h4.text for h4 in bloc_product.find('div',{'class':'infos-produit-2'}).find_all('h4')])
			p_html = bloc_product.find('div',{'class':'infos-produit-2'}).find('p')
			p_content = [p for p in p_html.text.split('\n') if p != '']
			if len(p_content) == 2:
				[package, unit_price_text] = p_content
			elif len(p_content) == 1:
				if u'€'  in p_content[0]:
					unit_price_text = p_content[0]
					package = ''
				else:
					package = p_content[0]
					unit_price = ''
			else:
				package = ''
				unit_price = ''

			[unit_price, unit] = unit_price_text.split(u'€/')
			unit_price = float(unit_price)

			product.update({
				'url': url,
				'reference': reference,
				'product_image_url': product_image_url,
				'brand': brand,
				'name': name,
				'unit_price': float(unit_price),
				'unit': unit
			})

			if not product['is_promotion']:
				price = float(bloc_product.find('div', {'class': 'prix-actuel'}).find('span').text.replace(u'€', ''))
				product['price'] = price
			else:
				promotion = {}
				if bloc_product.find('div',{'class': 'prix-old'}):
					before = float(bloc_product.find('div',{'class': 'prix-old'}).text.replace(u'€', ''))
					after = float(bloc_product.find('div',{'class': 'prix-promo'}).text.replace(u'€', ''))
				else:
					before = float(bloc_product.find('div',{'class': 'prix-actuel'}).find('span').text.replace(u'€', ''))
					after = before

				promotion ={
						'before': before,
						'after': after
					}
				product['promotion'] = promotion


			products.append(product)


		return products

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
		product = {
				'from': 'product_page',
				'is_promotion': False,
				'is_product': False,
				'is_available': True
			}
		parsed_page = self.parsed_page
		container = parsed_page.find('div', {'class': 'main-content'})
		if container:
			product_info = container.find(id='produit-infos')
			product_annexes =container.find(id = 'produit-infos-annexes') 
			html =  container.prettify()

			# Dealing with product infos
			brand = product_info.find('span', {'class': 'titre-principal'}).text
			name = product_info.find('span', {'class': 'titre-annexe'}).text
			complement = product_info.find('span', {'class': 'titre-secondaire'})
			if complement:
				complement = complement.text
			else:
				complement = ''
			product_image_url = product_info.find('img',{'class':'produit'}).attrs['src']
			if product_info.find('div',{'class': 'bientot-dispo'}):
				product['is_available'] = False

			product.update({
				'brand': brand,
				'name': name,
				'complement': complement,
				'product_image_url': product_image_url,
				'html': html
				})

			# Is this a promotion ?
			promotion = self.parse_promotion_full()
			if promotion == {}:
				# This is not a promotion
				product['is_product'] = True
				package = self.extract_package_content(product_info.find('span',{'class':'texte-info-normal'}).text.split('Composition : ')[1])
				price = float(product_info.find('div',{'class': 'prix-actuel'}).find('span').text.split(u'€')[0])
				[unit_price, unit] = product_info.find('div', {'class': 'prix-annexe'}).find('p').text.split(u'€/')
				unit_price = float(unit_price)
				product.update({
					'price': price,
					'unit_price': unit_price,
					'unit': unit,
					'package': package
					})

			else:
				product['is_promotion'] = True
				if promotion['type'] != 'multi':
					product['is_product'] = True

				product['promotion'] = promotion

			# Dealing with extra information
			if product['is_product']:
				information = {}
				information_block = product_annexes.find(id = 'panel-infos-detaillees')
				titles = information_block.find_all('h3')
				for title in titles:
					p = title.findNext('p')
					information[title.text] = p.text

				product['information'] = information


		else:
			print 'This is not a product page'

		return product

	def parse_promotion_full(self):
		"""
			This method extracts information form a promotion page, it includes all informations relative
			to the promotion

			Return:
				ref. parse_promotion_short. And other inofmration depending on osm
		"""
		parsed_page = self.parsed_page
		promotion = {}
		product_info = parsed_page.find(id='produit-infos')
		product_annexes =parsed_page.find(id = 'produit-infos-annexes') 
		promotion_composition  =  parsed_page.find(id = 'produit-composition')
		promotion_block = parsed_page.find('div', {'class':'promotion'})

		if promotion_composition:
			promotion['type'] = 'multi'
			# getting references to products in promotion
			products_block = promotion_composition.find_all('tr', {'class': 'bloc-produit-composition'})
			references = []
			for product_block in products_block:
				references.append(product_block.find('a').attrs['href'].split('/')[-1].split(';jsessionid=')[0])

			promotion['content'] = references
		else:
			full_text = self.extract_pure_text()
			if 'gratuit' in full_text:
				promotion['type'] = 'more'
			else:
				promotion['type'] = 'simple'


		if promotion_block:
			[unit_price, unit] = product_info.find('div', {'class': 'prix-annexe'}).find('p').text.split(u'€/')
			unit_price = float(unit_price)
			promotion['unit_price'] = unit_price
			promotion['unit'] = unit

			promotion_price_block = product_info.find('div',{'class': 'bloc-prix-promo'})
			if promotion_price_block:
				# Found old and promotion price
				before =float( promotion_price_block.find('span',{'class': 'prix-old'}).text.split(u'€')[0])
				after = float(promotion_price_block.find('span',{'class': 'prix-promo'}).text.split(u'€')[0])
				promotion.update({
					'before': before,
					'after': after
				})
			else:
				# Sometimes, only one price is found...
				price = float(product_info.find('div',{'class': 'prix-actuel'}).find('span').text.split(u'€')[0])
				promotion.update({
					'before': price,
					'after': price
				})

		return promotion

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

	def get_tags(self):
		"""
			Getting tags in category page.

			Output :
				- list of hash :
					{
						'name':...,
						'url':...
					}
		"""
		tags = []
		parsed_page = self.parsed_page

		as_tags = parsed_page.find_all(id=re.compile(r'viewSubCat(_\d+)?'))

		for a_tag in as_tags:
			name = a_tag.text
			if 'tous' != name.lower():
				tags.append({
					'name':a_tag.text,
					'url':a_tag.attrs['href']
					})

		return tags

