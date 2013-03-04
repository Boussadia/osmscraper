#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import simplejson as json

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

	def get_brands_values_in_category_page(self):
		"""
			In a category page, extract list of brands in a select field.

			Output :
				- list of hash : {'name': brand, value: 'brand_value'}
		"""
		parsed_page = self.parsed_page
		brands = []
		select = parsed_page.find(id = 'marquesListField')
		options = select.find_all('option')
		for o in options:
			value = o.attrs['value']
			name = o.text
			if value and value != '' and value != '-' and name:
				brands.append({
					'name': name,
					'value': value
					})

		return brands

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
		# Extracting products
		rows_html = parsed_page.find("table",{"class":"t-data-grid"}).find_all("td",{"class","descriptionCourtePanier"})


		for row in rows_html:
			for child in row.findChildren(recursive=False):
				if child.name == "li":
					try:
						product = {
							'is_product': False,
							'is_promotion': False,
							'is_available': True
						}
						html = child.prettify()
						url = child.findChildren(recursive=False)[0].get("href")
						name = child.findChildren(recursive=False)[0].find("img").get("alt")
						product_image_url = 'g-'.join(child.findChildren(recursive=False)[0].find("img").get("src").split('p-'))
						reference = url.split('/')[-1].split('-')[-1].split(';jsessionid=')[0]
						if 'LV' in reference:
							reference = reference.split('_')[1]
						product.update({
							'name': name,
							'url': url,
							'reference': reference,
							'html': html,
							'product_image_url': product_image_url
						})

						if child.find("p",{"class","promoPriceBox"}) is None:
							# Not a promotion, it is a simple product
							package_text = child.find('div', {'class': 'SubBox06'}).find_all('p')[2].find('span').text
							package = self.extract_package_content(package_text)
							product['package'] = package
							product["price"] = self.convert_to_float(child.find("p",{"class","priceBox"}).find("label").text)
							product['is_product'] = True
						else:
							# This is a promotion
							product['is_promotion'] = True
							product["promotion"] = self.parse_promotion_short(child)
							if product['promotion']['type'] == 'simple':
								product['is_product'] = True


						if len(self.strip_string(child.find("p",{"class":"Style06"}).text).split(" / ")) > 1:
							product["unit_price"], product["unit"] = self.strip_string(child.find("p",{"class":"Style06"}).text).split(" / ")
							product["unit_price"] = self.convert_to_float(product["unit_price"])
						else:
							product["unit_price"] = -1
							product["unit"] = "Unit"

						products.append( product )
					except Exception, e:
						print 'Error while scraping category page'
						print child.prettify()
						print e

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

		reference = product_html.find(id = 'productRef').attrs['value']

		# Price before and during promotion
		textContent = product_html.find('span', {'class': 'priceBox'}).find(text = True);
		promotion['after'] = self.convert_to_float(self.strip_string(textContent))

		textContent = product_html.find('del').find(text = True);
		promotion['before'] = self.convert_to_float(self.strip_string(textContent))

		# Date of promotion
		textContent = product_html.find('p', {'class':'offrePromo'}).find(text = True)
		regexp = '(\d{1,2})-(\d{1,2})-(\d{1,2})'
		[date_start, date_end] = re.findall(regexp, textContent)
		promotion['date_start'] = dict(zip(['day', 'month', 'year'], date_start))
		promotion['date_end'] = dict(zip(['day', 'month', 'year'], date_end))

		# Is it a simple or multi promotion?
		name = product_html.find('div', {'class': 'SubBox06'}).find_all('p')[1].find('span').text
		if 'lot :' in name.lower():
			type_promotion = 'multi'
		else:
			type_promotion = 'simple'

		promotion['type'] = type_promotion

		# Unit price
		promotion["unit_price"], promotion["unit"] = self.strip_string(product_html.find("p",{"class":"Style06"}).text).split(" / ")
		promotion["unit_price"] = self.convert_to_float(promotion["unit_price"])

		# Getting products references in promotion
		if type_promotion == 'simple':
			references = [product_html.findChildren(recursive=False)[0].get("href").split('-')[-1]]
		else:
			select = product_html.find(id = re.compile('varietyChoice(.*)'))
			if select:
				references = [ o.attrs['value']for o in select.find_all('option')]
			else:
				references = [product_html.findChildren(recursive=False)[0].get("href").split('_')[1]]

		promotion['references'] = references


		return promotion

	def parse_promotion_full(self):
		"""
			This method extracts information form a promotion page, it includes all informations relative
			to the promotion

			Return:
				ref. parse_promotion_short. And other inofmration depending on osm
		"""
		promotion = {}
		promotion_html = self.parsed_page.find(id='ficheProduit')

		# Reference of promotion
		reference = promotion_html.find(id = 'productRef').attrs['value']
		if 'LV' in reference:
			reference = reference.split('_')[1]
		promotion['reference'] = reference

		# Getting price before and after promotion
		price_block = promotion_html.find('p', {'class' : 'promoPriceBox'})
		price_after = self.convert_to_float(price_block.find('span').text)
		price_before = self.convert_to_float(price_block.find('del').text)
		promotion['before'] = price_before
		promotion['after'] = price_after

		# dates of promotion
		date_block = promotion_html.find('p', {'class':'offrePromo'})
		results = re.findall(r'(\d{1,2})-(\d{1,2})-(\d{1,2})', date_block.text)
		promotion.update(dict(zip(['date_start', 'date_end'], [ dict(zip(['day','month', 'year'], r)) for r in results])))

		# Is this a multi promotion?
		promotion_infos = promotion_html.find('div', {'class': 'promo'})
		if promotion_infos:
			promotion_infos = promotion_infos.find('p', {'class': 'Style05'})
			if promotion_infos:
				textContent = promotion_infos.text

				if 'lot ' in textContent.lower():
					promotion['type'] = 'multi'
				else:
					promotion['type'] = 'simple'

		promotion["unit_price"], promotion["unit"] = self.strip_string(promotion_html.find("p",{"class":"Style06"}).text).split(" / ")
		promotion["unit_price"] = self.convert_to_float(promotion["unit_price"])

		# References of product
		if promotion['type'] == 'simple':
			references = [reference]
		else:
			select = promotion_html.find(id = re.compile('varietyChoice(.*)'))
			if select:
				references = [ o.attrs['value']for o in select.find_all('option')]
			else:
				references = [reference]

		promotion['references'] = references



		

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
			'is_available': True
		}
		parsed_page = self.parsed_page
		product_section = parsed_page.find(id="ficheProduit")

		if product_section is not None:
			html = product_section.prettify()
			product['html'] = html
			product_infos = product_section.find("div",{"class","InfoProduit"})

			product["name"] = self.strip_string(product_infos.find("p",{"class":"Style02"}).text)

			# Is it a promotion?
			if product_section.find('p', {'class': 'promoPriceBox'}):
				product['promotion'] = self.parse_promotion_full()
				product['is_promotion'] = True

				if product['promotion']['type'] == 'simple':
					product['is_product'] = True
			else:
				product['is_product'] = True
				product["price"] = self.convert_to_float(product_section.find("p",{"class","priceBox"}).find("label").text)
			
			if product['is_product']:
				package_text = self.strip_string(product_infos.find("p",{"class":"Style03"}).text)
				package = self.extract_package_content(package_text)
				product['package'] = package

			if len(self.strip_string(product_section.find("p",{"class":"Style06"}).text).split(" / ")) > 1:
				product["unit_price"], product["unit"] = self.strip_string(product_section.find("p",{"class":"Style06"}).text).split(" / ")
				product["unit_price"] = self.convert_to_float(product["unit_price"])
			else:
				product["unit_price"] = -1
				product["unit"] = "Unit"

			product["product_image_url"] = product_section.find("div",{"class","InfoProduitExtra"}).find("div",{"class","ContentCenterSubWrap"}).find("img").get("src")

			lis = product_section.find("ul",{"class","Accordion02"}).find_all("li")
			product['information'] = {}

			for i in xrange(0,len(lis)):
				li = lis[i]
				product['information'][li.find("h4").text] = li.find("p",{"class","Para04"}).text
		else:
			product["status"] = 404
			product['is_product'] = False
			product['exists'] = False

		return product

	#-----------------------------------------------------------------------------------------------------------------------
	#
	#									SPECIFIC METHODS TO MONOPRIX PARSER
	#
	#-----------------------------------------------------------------------------------------------------------------------

	def pagination_link_all(self):
		"""
			Getting link to page that displays all products for a category page

			Output : 
				- current_page_is_all (boolean) : si la page actuelle contient deja tous les produits = False
				- url : link to all products page 
		"""
		parsed_page = self.parsed_page
		current_page_is_all = False
		url_all_products = ""


		active_pagination = parsed_page.find("div", {"class","PageViewControl"}).find("li",{"class":"Active"}).text
		if active_pagination != "Tous":
			links = parsed_page.find("div", {"class","PageViewControl"}).find_all("a")
			for link in links:
				if link.get("title") == "Tous":
					url_all_products = link.get("href")
					current_page_is_all = True
					break

		return current_page_is_all, url_all_products

	def get_postal_code_form_data(self):
		"""
			This methid extracts from a monoprix page the form data to set location.

			Output :
				- hash : {name: value}
		"""
		parsed_page = self.parsed_page
		form = parsed_page.find(id = re.compile(r'formZipCode(.*)'))
		inputs = form.find_all('input')
		data = {'url':form.attrs['action'], 'data': {}}
		for input in inputs:
			if 'name' in input.attrs:
				name = input.attrs['name']
				if 'value' in input.attrs:
					value =  input.attrs['value']
				else:
					value = None
				data['data'][name] = value

		return data

	def get_form_delivery_zone(self):
		"""
			Check the html in order to determine what step of the process of the address setting we are on

			Output :
				- data = {
							'type': 'select' or 'address',
							'form': {
								'url' : rul of form
								'data' : {data to pass to requery}
							}
						}

		"""
		data = {'type': None}
		parsed_page = self.parsed_page
		div_delivery = parsed_page.find(id = 'deliveryZone')

		# Is the form to select delivery/click & go/drive here?
		form_delivery = div_delivery.find(id = re.compile(r'formRadioDelivery(.*)'))
		if form_delivery:
			inputs = form_delivery.find_all('input')
			data = {'type' : 'select', 'form': {'url':form_delivery.attrs['action'], 'data': {}}}
			for input in inputs:
				if 'name' in input.attrs:
					name = input.attrs['name']
					if 'value' in input.attrs:
						value =  input.attrs['value']
					else:
						value = None
					if name in data['form']['data']:
						if type(data['form']['data'][name]) == type([]):
							data['form']['data'][name].append(value)
						else:
							data['form']['data'][name] = [data['form']['data'][name], value]
					else:
						data['form']['data'][name] = value
		else:
			# Is it a non served area?
			textDelivery = div_delivery.text
			if textDelivery == '':
				# Is there a form to add address ?
				div_qas = parsed_page.find(id = 'qasZone')
				form_address = div_qas.find(id = re.compile(r'addressForm(.*)'))
				if form_address:
					inputs = form_address.find_all('input')
					data = {'type' : 'address', 'form': {'url':form_address.attrs['action'], 'data': {}}}
					for input in inputs:
						if 'name' in input.attrs:
							name = input.attrs['name']
							if 'value' in input.attrs:
								value =  input.attrs['value']
							else:
								value = None
							data['form']['data'][name] = value

		return data

	def extract_suggested_addresses(self, data):
		"""
			When providing Monoprix with an adress, they need the user to click on the address sugested by server.
			This method parses the json retrieved from server and return lists of suggestions and links to activate in order to 
			validate address

			Input : 
				- data (string) : example -> 
					{
						"content":"",
						"scripts":["http://docs.monoprix.fr/assets/ctx/monoprixV2-1/static/javascript/generic_zone_updater.js","http://pics.monoprix.fr/assets/ctx/monoprixV2-1/static/javascript/generic_zone_updater.js"],
						"script":"jQuery('input[name=\"addressQAS\"]').removeClass('FieldError');\ndefaultGenericZoneUpdater = new GenericZoneUpdater({\"elementId\":\"addressSuggestId-13ccd8c1b52\",\"event\":\"click\",\"zone\":\"qasZone\",\"url\":\"/productlist.popupcontainer.popupident.popupidentaddress.qassearchaddress.addresssuggestid:addressselected/FRI$007c4507389$007c0MOFRIBQzcBwAAAAAIAwEAAAAEGBeyAAAAAAABADE1ADE1AGQAAAAA.....wAAAAAAAAAAAAAAAAAxNSBib3VsZXZhcmQgZGUgLCA3NTAwMSAA\",\"fields\":[]})\ndefaultGenericZoneUpdater = new GenericZoneUpdater({\"elementId\":\"addressSuggestId-13ccd8c1b52_0\",\"event\":\"click\",\"zone\":\"qasZone\",\"url\":\"/productlist.popupcontainer.popupident.popupidentaddress.qassearchaddress.addresssuggestid:addressselected/FRI$007c4507389$007c0MOFRIBQzcBwAAAAAIAwEAAAAEGBc_gAAAAAABADE1ADE1AGQAAAAA.....wAAAAAAAAAAAAAAAAAxNSBib3VsZXZhcmQgZGUgLCA3NTAwMSAA\",\"fields\":[]})\n",
						"zones":{
							"noAddressResultsZone":"",
							"QASResultZone":"<div class='autoadresse3 SelectUI Theme_Monoprix Theme_Modify Theme_FirstItem HasSelectUI'><ul><li id='addressSuggestId-13ccd8c1b52'>15 BOULEVARD DE LA MADELEINE, 75001 PARIS<\/li><li id='addressSuggestId-13ccd8c1b52_0'>15 BOULEVARD DE SEBASTOPOL, 75001 PARIS<\/li><\/ul><\/div>"
						}
					}
			Output : 
				- list [('addressSuggestId-13ccd8c1b52', '/productlist.popupcontainer.popupident.popupidentaddress.qassearchaddress.addresssuggestid:addressselected/FRI$007c4507389$007c0MOFRIBQzcBwAAAAAIAwEAAAAEGBeyAAAAAAABADE1ADE1AGQAAAAA.....wAAAAAAAAAAAAAAAAAxNSBib3VsZXZhcmQgZGUgLCA3NTAwMSAA'), ('addressSuggestId-13ccd8c1b52_0', '/productlist.popupcontainer.popupident.popupidentaddress.qassearchaddress.addresssuggestid:addressselected/FRI$007c4507389$007c0MOFRIBQzcBwAAAAAIAwEAAAAEGBc_gAAAAAABADE1ADE1AGQAAAAA.....wAAAAAAAAAAAAAAAAAxNSBib3VsZXZhcmQgZGUgLCA3NTAwMSAA')]

		"""
		# Converting to python dictionnary
		data =json.loads(data)
		suggestions = []
		if data['zones']['noAddressResultsZone'] == "":
			# Some suggestions where found
			# Now we extract id and path to validate address
			reg = r'"elementId":"(addressSuggestId-\w+)",".*","url":"(/productlist.popupcontainer.popupident.popupidentaddress.qassearchaddress.addresssuggestid:addressselected/.*)","'
			results = re.findall(reg, data['script'])

			# Now looking for address corresponding to id retrieved
			html = data['zones']['QASResultZone']
			self.set_html(html)
			for id, path in results:
				address =  self.parsed_page.find(id=id).text
				suggestions.append({
					'id': id,
					'url': path,
					'address': address
					})
		return suggestions

		
