#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from urlparse import urlparse, parse_qs

from scrapers.base.baseparser import BaseParser

class MonoprixParser(BaseParser):
	"""
		Monoprix parser

	"""

	def __init__(self, html = ''):
		super(MonoprixParser, self).__init__(html)

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
			menu_li = self.parsed_page.find(id="h_n-1").find_all("li")

			# Getting main categories
			for li in menu_li:
				class_li = li.get("class")
				name = li.find("a").get("title")
				url = li.find("a").get("href")
				if ('Reverse' not in class_li) and name != "MODE":
					print "Found main category : "+name
					categories.append({
						'name': name,
						'url':url,
					})

		elif level == 1:
			categories_html = self.parsed_page.find("ul",{"class","SideNav"}).find("li",{"class","Active"}).find("ul").find_all("li")

			for i in xrange(0,len(categories_html)):
				category_html = categories_html[i]
				name = category_html.find("a").get("title")
				url = category_html.find("a").get("href")
				print "Found sub category : "+name
				categories.append({
					'name': name,
					'url':url,
				})
		elif level == 2:
			categories_html = self.parsed_page.find(id="topNavigation").find("ul",{"class","N3"})
			lis = categories_html.find_all("li")
			for i in xrange(0,len(lis)):
				li = lis[i]
				name = li.find("a").get("title")
				url = li.find("a").get("href")
				print "Found sub category level 2 "+name
				categories.append({
					'name': name,
					'url':url,
				})

		elif level == 3:
			ul = self.parsed_page.find(id="topNavigation").find("ul",{"class","N4"})
			if ul  is not None:
				lis = ul.find_all("li")

				for i in xrange(0,len(lis)):
					li = lis[i]
					name = li.find("a").get("title")
					url = li.find("a").get("href")
					print "Found sub category level 3 "+name
					categories.append({
						'name': name,
						'url':url,
					})

		return categories

	def get_pagination(self):
		"""
			This method extracts from a cartegory page the pagination.

			Output :
				- list of hash representing pagination : {'url': url, 'page': 2}
		"""
		parsed_page = self.parsed_page
		pagination = []
		
		# Is there more than one page of products for this category? (pagination)
		form_parsed = parsed_page.find(id='aspnetForm')
		pagination_links = parsed_page.find_all('a',{'class': 'rptPagination'}) # Should be an even number (pagination at the top and bottom of the page)
		pagination_links = pagination_links[:len(pagination_links)/2] # removing unecessary elements

		for i in xrange(0,len(pagination_links)):
			if 'href' in pagination_links[i].attrs:
				eventTarget =  pagination_links[i].attrs['href'].split("javascript:__doPostBack('")[1].split("','")[0]
				eventArgument = pagination_links[i].attrs['href'].split("javascript:__doPostBack('")[1].split("','")[1].split("')")[0]
				pagination.append({"page":(i+1), "eventTarget": eventTarget, "eventArgument": eventArgument})
			else:
				pagination.append({"page":(i+1)})

		return pagination

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
		parsed_page = self.parsed_page
		products = []
		lis = parsed_page.find_all('li',{'class':'lineproductLine'}) # products in li
		
		for i in xrange(0, len(lis)):
			product = {
					'is_product': False,
					'is_promotion': False,
					'is_available': False
				}
			try:
				li = lis[i]
				product['html'] = li.prettify()

				name = li.find('h5').find(text=True)[22:-40]
				brand = li.find('img', {'class':'marque'})
				brand_image_url = brand.attrs['src']
				if 'title' in brand.attrs:
					brand = brand.attrs['title']
				else:
					brand = '' # Some products do not have brands

				image_url = li.find('input', {'class':'image'}).attrs['src'].replace('Vignettes', 'Images')
				url = li.find('a', {'class':'prodimg'}).attrs['href']
				scheme, netloc, path, params, query, fragment = urlparse(url)
				reference = parse_qs(query)['NOEUD_IDFO'][0]

				# Is the product available
				if li.find('img', {'class': 'indispo'}):
					product['is_available'] = False
				else:
					product['is_available'] = True

				product.update({
					'name': name,
					'brand': brand,
					'brand_image_url': brand_image_url,
					'product_image_url': image_url,
					'url': url,
					'reference': reference
				})

				# Default value of is_product
				product['is_product'] = True

				# Dealing with promotion
				if 'Promo' in li.attrs['class']:
					product['is_promotion'] = True
					promotion = self.parse_promotion_short(li)
					product['promotion'] = promotion
					if promotion['type'] == 'multi':
						product['is_product'] = False
				else:
					textContent = li.find('strong').find(text=True)
					product['price'] = self.convert_to_float(self.strip_string(textContent))

					textContent = li.find(id = re.compile(r'ctl00_cphC_pn3T1_ctl01_rp_ctl(\d+)_ctl00_lPrxUnit')).find(text=True)

					product['unit_price'] = float(textContent.split(u' € / ')[0].replace(u',', u'.'))
					product['unit'] = textContent.split(u' € / ')[1]

					textContent = li.find(id = re.compile(r'ctl00_cphC_pn3T1_ctl01_rp_ctl(\d+)_ctl00_lCont')).find(text=True)
					product['package'] =self.extract_package_content(textContent)

				
				products.append(product)
			except Exception, e:
				print 'ERROR PARSING PRODUCT : '+str(e)
		return products

	def parse_promotion_short(self, product_html):
		"""
			This method is responsible for extracting information regarding promotion in a product form a category page.

			Input :
				- product_html (BeautifulSoup object) : the product_html to analyse
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
		promotion = {}

		textContent = product_html.find('strike').find(text = True);
		promotion['before'] = self.convert_to_float(self.strip_string(textContent))

		textContent = product_html.find('strong').find(text = True);
		promotion['after'] = self.convert_to_float(self.strip_string(textContent))

		textContent = product_html.find(id = re.compile(r'ctl00_cphC_pn3T1_ctl01_rp_ctl(\d+)_ctl00_lPrxUnit')).find(text=True)

		promotion['unit_price'] = float(textContent.split(u' € / ')[0].replace(u',', u'.'))
		promotion['unit'] = textContent.split(u' € / ')[1]

		if promotion['unit'] == 'Lot':
			promotion['type'] = 'multi'
		else:
			promotion['type'] = 'simple'
			textContent = product_html.find(id = re.compile(r'ctl00_cphC_pn3T1_ctl01_rp_ctl(\d+)_ctl00_lCont')).find(text=True)
			promotion['package'] =self.extract_package_content(textContent)

		return promotion

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
			match = re.search(r'(\d+),?(\d*) ?\W ?/ ?(\w{1,10})', text)
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
					promotion['product_image_urls'] = [p.find('a').find('img').attrs['src'].replace('Vignettes', 'Images') for p in products_lot]


				else:
					# Simple promotion
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
			if img_unavailable:
				product['is_available'] = False
			else:
				product['is_available'] = True

			# Extracting product name and brand
			name_and_brand = product_html.find('h3', {'class', 'BmarginSm'}).find(text=True)
			# Cleaning from spaces and carriage return
			name_and_brand = re.search('(\\n| |\\r\\n)+(.*)(\\n| |\\r\\n)*', name_and_brand).group(2)
			# Seperating name and brand
			if '-' in name_and_brand:
				name_and_brand = name_and_brand.split(' - ')
				product['name'] = ' - '.join(name_and_brand[:-1])
				product['brand'] = name_and_brand[-1:][0]
			else:
				product['name'] = name_and_brand
				product['brand'] = '' # Some products do not have brands...

			# Getting images
			product_image = self.parsed_page.find(id='ctl00_cphC_pn3T1_ctl01_imgVisu')
			product_image_url = product_image.attrs['src']
			brand_image = self.parsed_page.find(id='ctl00_cphC_pn3T1_ctl01_iLogo')
			brand_image_url = brand_image.attrs['src']
			product['product_image_url'] = product_image_url
			product['brand_image_url'] = brand_image_url

			# Checking if promotion
			rects_html = product_html.find_all('a', {'class': 'btnRectSimple'})
			promotion_html = None
			for rect in rects_html:
				text = ' '.join(rect.find_all(text=True)).lower()
				if 'promotion' in text:
					promotion_html = rect
			if promotion_html:
				# This product is a promotion
				product['is_promotion'] = True
				product['promotion'] = self.parse_promotion_full()
				if product['promotion']['type'] == 'simple':
					product['is_product'] = True
				else:
					product['is_product'] = False
			else:
				product['is_product'] = True

			if product['is_product']:
				# Getting base product information
				product_info = self.parsed_page.find(id='ctl00_cphC_pn3T1_ctl01_divContentPromNouv')

				if not product['is_promotion']:
					# Getting price
					price = product_info.find('p', {'class', 'price'}).find('strong').find(text= True)
					product['price'] = self.convert_to_float(price)

				# Getting package content unit price and unit
				product_info_ps = product_info.find_all('p')
				for p in product_info_ps:
					if 'class' not in p.attrs:
						text = p.find(text=True)
						# Appyling reg
						match = re.search(r'(\d+),?(\d*) ?\W ?/ ?(\w{1,10})', text)
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
		regexp2 = r'(\d+)(?!,)[^\d]+(\d+,?\d*) ?(\w+)' # type = les 3 boites de 200g
		regexp3 = r'(\d+,?\d*) ?(\w+)' # type = La bouteille de 1,5L
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
						'quantity': 1,
						'quantity_measure': self.convert_to_float(m.group(1)),
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
