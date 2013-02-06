#!/usr/bin/python
# -*- coding: utf-8 -*-

from urlparse import urlparse, parse_qs, urlunparse

from scrapers.base.basescraper import BaseScraper
from scrapers.ooshop.ooshopparser import OoshopParser
from scrapers.ooshop.ooshopcrawler import OoshopCrawler
from scrapers.ooshop.ooshopdatabasehelper import OoshopDatabaseHelper

class OoshopScraper(BaseScraper):
	"""
		docstring for OoshopScraper
	"""
	def __init__(self):
		super(OoshopScraper, self).__init__('http://www.ooshop.com', OoshopCrawler, OoshopParser, OoshopDatabaseHelper)

	def get_all_categories(self):
		"""
			Categories process, specific to child class.
		"""
		url = self.base_url
		categories = []

		# Getting main and sub categories level 1
		html, code = self.crawler.get(url)
		if code == 200:
			self.parser.set_html(html)
			categories = self.parser.get_categories(level = 0)
		else:
			print "Something went wrong when fetching main categories for Ooshop"

		# Categories is a list of main categories and sub categories level 1
		# Cycle through level 1 categories keep going till level 3

		for i in xrange(0, len(categories)):
			main_category = categories[i]

			for j in xrange(0, len(main_category['sub_categories'])):
				level_1_category = main_category['sub_categories'][j]
				url = self.base_url + '/' + level_1_category['url']
				html, code = self.crawler.get(url)
				if code == 200:
					self.parser.set_html(html)
					level_1_category['sub_categories'] = self.parser.get_categories(level = 2)

					# We have to fetch sub categories level 3 here because of the way Ooshop website works
					for k in xrange(0, len(level_1_category['sub_categories'])):
						level_2_category = level_1_category['sub_categories'][k]
						url = self.base_url + '/' + level_2_category['url']
						html, code = self.crawler.get(url)
						if code == 200:
							self.parser.set_html(html)
							level_2_category['sub_categories'] = self.parser.get_categories(level = 3)
						else:
							print "Something went wrong when fetching level 3 categories for Ooshop"

				else:
					print "Something went wrong when fetching level 2 categories for Ooshop"
		
		# Here we pass the categories list to the databasehelper to be saved
		# TO DO

	def is_served_area(self, code_postal = '94230'):
		"""
			This method checks if a given area is served by ooshop.

			Input :
				- code_postal (string) : french postal code of a city.
			Output:
				- boolean : True -> served, False -> not served
				- code : was the request successfull? (200 = OK)
		"""
		is_served = False

		# Verification url
		url = 'http://www.ooshop.com/courses-en-ligne/WebForms/Utilisateur/VerifEligibilite.aspx'
		html, code = self.crawler.get(url)
		if code == 200:
			self.parser.set_html(html)
			form_data = self.parser.get_form_values()
			# Setting postal code argument to the one povided & other necessary post value
			form_data['ctl00$cphC$elig$tbCp'] = code_postal
			form_data['ctl00$sm'] = 'ctl00$sm|ctl00$cphC$elig$bEli'
			form_data['__EVENTTARGET'] = ''
			form_data['__EVENTARGUMENT'] = ''
			form_data['__LASTFOCUS'] = ''
			form_data['ctl00$xCoordHolder'] = 0
			form_data['ctl00$yCoordHolder'] = 281

			# Deleting unecessary post argument
			del form_data['ctl00$cphC$elig$ValiderEmail2']
			del form_data['ctl00$headerCtrl$btOK']
			del form_data['ctl00$cphC$elig$lv$LoginButton']
			del form_data['ctl00$Perso$ucAu$ValiderEmail']
			del form_data['ctl00$Perso$ucAu$SubmitButton']
			del form_data['ctl00$Perso$ucAu$lv$LoginButton']
			del form_data['ctl00$ucDetProd$AjoutPanier1$btPan']

			# geting response
			html, code = self.crawler.post(url, data = form_data)
			
			if code == 200:
				# Parsing html
				self.parser.set_html(html)
				is_served = self.parser.get_eligibility()
			else:
				print 'Error %d'%(code)

		else:
			print 'Something went wrong : error %d'%(code)

		return is_served, code



	def get_all_products(self):
		"""
			Retrives all possible localisation, retrieves all categories and fetches all products for
			each localisation and saves them.
		"""
		pass

	def get_localized_product(self, localisation):
		pass



	def get_product_info(self, product_url):
		"""
			Retrive complete information for product. Independent from localisation.

			Input : 
				- product_url (string) :  url of product to scrape
			Output :
				- hash representing the product 
				- code (int) : was the request successfull (200 = OK)
		"""
		# First, retrieve html page
		html, code = self.crawler.get(product_url)

		if code == 200:
			self.parser.set_html(html)
			product = self.parser.parse_product_full()

			# Adding reference to product hash
			if product['is_product']:
				scheme, netloc, path, params, query, fragment = urlparse(product_url)
				product['reference'] = parse_qs(query)['NOEUD_IDFO'][0]
				product['url'] = product_url

				# Setting proper full urls
				product['brand_image_url'] = urlunparse((scheme, netloc, product['brand_image_url'], '', '', ''))
				product['product_image_url'] = urlunparse((scheme, netloc, product['product_image_url'], '', '', ''))
			print product
			# TO DO : save product in database
		else:
			print 'Error while retrieving product page : error %d'%(code)


		# products = []
		# lis = parsed_page.find_all('li',{'class':'lineproductLine'}) # products in li
		# self.total_products_found = self.total_products_found + len(lis)
		
		# for i in xrange(0, len(lis)):
		# 	try:
		# 		li = lis[i]
		# 		name = li.find('h5').find(text=True)[22:-40]
		# 		brand = li.find('img', {'class':'marque'}).attrs['title']
		# 		image_url = self.get_base_url()+'/'+li.find('input', {'class':'image'}).attrs['src'].replace('Vignettes', 'Images')
		# 		url = self.get_base_url()+'/'+li.find('a', {'class':'prodimg'}).attrs['href']
		# 		reference = image_url.split('/')[-1].split('.')[0]

		# 		product = {
		# 			'name': name,
		# 			'brand': brand,
		# 			'image_url': image_url,
		# 			'url': url,
		# 			'reference': reference
		# 		}

		# 		# Dealing with promotion

		# 		promotion = {}
		# 		if 'Promo' in li.attrs['class']:
		# 			textContent = li.find('strike').find(text = True);
		# 			product['price'] = float(textContent[17:-2].replace(',', '.'))

		# 			textContent = li.find('strong').find(text = True);
		# 			promotion['percentage'] = 1 - float(textContent[17:-2].replace(',', '.')) / product['price']
					
		# 			ps = li.find('div',{'class' : 'unit price'}).find_all('p') #  p:not(.productPicto) span')[0].textContent
		# 			if 'productPicto' in ps[0].attrs['class']:
		# 				p = ps[1]
		# 			else:
		# 				p = ps[0]

		# 			textContent = p.find('span').find(text=True)
		# 			product['unit_price'] = float(textContent.split(u' € / ')[0].replace(u',', u'.'))
		# 			product['unit'] = textContent.split(u' € / ')[1]

		# 			textContent = p.find_all('span')[1].find(text=True)
		# 			product['text_unit'] = textContent

		# 			if product['unit'] == 'Lot':
		# 				promotion['type'] = 'lot'
		# 				promotion['selector'] = '.lineproductLine:nth-child('+unicode(2*(i+1)-1)+') a.prodimg'
		# 				promotion['references'] = self.get_references(product['url'])
		# 			else:
		# 				promotion['type'] = 'simple'

		# 		else:
		# 			promotion['type'] = 'none'
		# 			textContent = li.find('strong').find(text=True)
		# 			product['price'] = float(textContent[17:-2].replace(',', '.'))

		# 			ps = li.find('div',{'class' : 'unit price'}).find_all('p') #  p:not(.productPicto) span')[0].textContent
		# 			if 'class' in ps[0].attrs and 'productPicto' in ps[0].attrs['class']:
		# 				p = ps[1]
		# 			else:
		# 				p = ps[0]

		# 			textContent = p.find('span').find(text=True)
		# 			product['unit_price'] = float(textContent.split(u' € / ')[0].replace(u',', u'.'))
		# 			product['unit'] = textContent.split(u' € / ')[1]

		# 			textContent = p.find_all('span')[1].find(text=True)
		# 			product['text_unit'] = textContent

		# 		product['promotion'] = promotion
		# 		products.append(product)
		# 	except Exception, e:
		# 		print 'ERROR PARSING PRODUCT : '+str(e)

		# return products


	def is_available(self, product_url):
		"""
			This method checks if the product is still available in the osm website
		"""
		pass

	def what_to_do_next(self):
		"""
			Defines the logic of the scraper.
		"""
		pass		