#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, urllib2
from bs4 import BeautifulSoup
import re

from osmscraper import OSMScraper


class Ooshop(OSMScraper):
	"""
		Parser for Online SuperMarket Ooshop.com
	"""
	def __init__(self):
		super(Ooshop, self).__init__("http://www.ooshop.com/courses-en-ligne")
		self.total_products_found = 0
		

	def get_menu(self):
		parsed_page, code, cookie = self.get_parsed_page_for_url_cookie()

		if code == 200:

			# Getting main categories and sub categories level 1
			a_main_menu= parsed_page.find_all("a",{"class":re.compile("univ(\d){1}")})
			li_sub = parsed_page.find(id="navh").find_all("li")
			print "Main menu contains "+str(len(a_main_menu))+" categories."
			categories = {}

			for i in xrange(0,len(li_sub)):
				li = li_sub[i]
				a_main_cats = li.find_all("a",{"class":re.compile("univ(\d){1}")})
				if len(a_main_cats)>0:
					a = a_main_cats[0]
					title = a.find(text=True)
					url = a.get("href")
					categories[title] = {
						'url':url,
						'cookie': cookie,
						'sub_categories':{}
					}

					sub_cats = li.find("div").find_all("a")

					print "Found "+str(len(sub_cats))+" sub categories for main category "+title

					sub_categories = {}
					
					for j in xrange(0, len(sub_cats)):
						print "Found category "+sub_cats[j].findAll(text=True)[0][2:]
						sub_categories[sub_cats[j].findAll(text=True)[0][2:]] = {
							"url" : sub_cats[j].get("href"),
							'cookie': cookie,
							'sub_categories':{}
						}
					categories[title]["sub_categories"] = sub_categories

			self.set_categories(categories)

			# Getting sub categories level 2
			self.get_sub_menu_level_2()

			# Getting sub categories level 3
			self.get_sub_menu_level_3()

		else:
			print "Aborting scraping main categories"

	def get_sub_menu_level_2(self):
		categories = self.get_categories()
		for title, category in categories.iteritems():
			# In main categories
			sub_categories_level_1 = category["sub_categories"]

			for title_sub_category_level_1, sub_category_level_1 in sub_categories_level_1.iteritems():
				url_sub_category_level_1 = sub_category_level_1["url"]
				parsed_page, code, cookie = self.get_parsed_page_for_url_cookie(url_sub_category_level_1)
				sub_categories_level_2 ={}					

				if code == 200:
					lis = parsed_page.find(id = "ctl00_cphC_ns_rpFilTab_ctl01_ucBns_p1" ).find_all("li")

					print "Found "+str(len(lis))+" sub categories level 2 for sub category "+title_sub_category_level_1

					for i in xrange(0, len(lis)):
						li = lis[i]
						title_sub_category_level_2 = li.find("a").find(text=True)
						url_sub_category_level_2 = li.find("a").get("href")
						sub_categories_level_2[title_sub_category_level_2] ={
							"url": url_sub_category_level_2,
							"sub_categories":{},
							"cookie": cookie,
						}
					categories[title]["sub_categories"][title_sub_category_level_1]["sub_categories"] = sub_categories_level_2
				else:
					print "Aborting scraping sub categories level 2"

		self.set_categories(categories)

	def get_sub_menu_level_3(self, cookie = None):
		categories = self.get_categories()
		for title, category in categories.iteritems():
			# In main categories
			sub_categories_level_1 = category["sub_categories"]

			for title_sub_category_level_1, sub_category_level_1 in sub_categories_level_1.iteritems():
				sub_categories_level_2 = sub_category_level_1["sub_categories"]

				for title_sub_category_level_2, sub_category_level_2 in sub_categories_level_2.iteritems():
					url_sub_category_level_2 = sub_category_level_2["url"]
					cookie = sub_category_level_2["cookie"]
					parsed_page, code, cookie = self.get_parsed_page_for_url_cookie(url_sub_category_level_2, cookie)
					sub_categories_level_3 ={}

					if code == 200:
						div = parsed_page.find(id="ctl00_cphC_ns_rpFilTab_ctl02_ucBns_p1")
						if div is not None:
							lis = div.find_all("li")
							print "Found "+str(len(lis))+" sub categories level 3 for sub categories level 2 "+title_sub_category_level_2

							for i in xrange(0, len(lis)):
								li = lis[i]
								title_sub_category_level_3 = li.find("a").find(text=True)
								url_sub_category_level_3 = li.find("a").get("href")
								sub_categories_level_3[title_sub_category_level_3] ={
									"url": url_sub_category_level_3,
									"cookie": cookie
								}
							categories[title]["sub_categories"][title_sub_category_level_1]["sub_categories"][title_sub_category_level_2]["sub_categories"] = sub_categories_level_3

					else:
						print "Aborting scraping sub categories level 3"
		self.set_categories(categories)

	def get_products_for_category(self, category):
		url = category["url"]
		cookie = category["cookie"]
		products = self.get_product_list_for_url_category(url, cookie)
		return products

	def get_product_list_for_url_category(self, url_category, cookie='xtvrn=$460644$; vuidck=6b124715-62fb-4903-bc7b-fa8994716724; SupportCookies=true; atgPlatoStop=1; OOshopSessionState=dcu0rp450bxhq5ba2dmelf55; s_cc=true; xtan460644=-; xtant460644=1; fs_nocache_guid=0EBDF3490718C0957774FA88BFE3CC97; s_sq=%5B%5BB%5D%5D; s_vi=[CS]v1|2857A04005160775-6000018360002F45[CE]; juniper=18faf872ea4792ef9af05da1b3681935'):
		parsed_page, code = self.get_parsed_page_for_url(url_category)
		products = []

		if code == 200:
			# Is there more than one page of products for this category? (pagination)
			form_parsed = parsed_page.find(id='aspnetForm')
			pagination_links = parsed_page.find_all('a',{'class': 'rptPagination'}) # Should be an even number (pagination at the top and bottom of the page)
			pagination_links = pagination_links[:len(pagination_links)/2] # removing unecessary elements

			post_data_to_perform = []
			products = self.get_product_list_from_parsed_page(parsed_page)

			for i in xrange(0,len(pagination_links)):
				if 'href' in pagination_links[i].attrs:
					eventTarget =  pagination_links[i].attrs['href'].split("javascript:__doPostBack('")[1].split("','")[0]
					eventArgument = pagination_links[i].attrs['href'].split("javascript:__doPostBack('")[1].split("','")[1].split("')")[0]
					post_data_to_perform.append({"eventTarget": eventTarget, "eventArgument": eventArgument, "form_parsed": form_parsed})
					products = products + self.get_product_list_from_parsed_page(self.__do_PostBack(eventTarget, eventArgument, form_parsed, cookie))
			
		else:
			print "Aborting fetch of products list"

		return products

	def get_product_list_from_parsed_page(self, parsed_page):
		products = []
		lis = parsed_page.find_all('li',{'class':'lineproductLine'}) # products in li
		self.total_products_found = self.total_products_found + len(lis)
		
		for i in xrange(0, len(lis)):
			try:
				li = lis[i]
				name = li.find('h5').find(text=True)[22:-40]
				brand = li.find('img', {'class':'marque'}).attrs['title']
				image_url = self.get_base_url()+'/'+li.find('input', {'class':'image'}).attrs['src'].replace('Vignettes', 'Images')
				url = self.get_base_url()+'/'+li.find('a', {'class':'prodimg'}).attrs['href']
				reference = image_url.split('/')[-1].split('.')[0]

				product = {
					'name': name,
					'brand': brand,
					'image_url': image_url,
					'url': url,
					'reference': reference
				}

				# Dealing with promotion

				promotion = {}
				if 'Promo' in li.attrs['class']:
					textContent = li.find('strike').find(text = True);
					product['price'] = float(textContent[17:-2].replace(',', '.'))

					textContent = li.find('strong').find(text = True);
					promotion['percentage'] = 1 - float(textContent[17:-2].replace(',', '.')) / product['price']
					
					ps = li.find('div',{'class' : 'unit price'}).find_all('p') #  p:not(.productPicto) span')[0].textContent
					if 'productPicto' in ps[0].attrs['class']:
						p = ps[1]
					else:
						p = ps[0]

					textContent = p.find('span').find(text=True)
					product['unit_price'] = float(textContent.split(u' € / ')[0].replace(u',', u'.'))
					product['unit'] = textContent.split(u' € / ')[1]

					textContent = p.find_all('span')[1].find(text=True)
					product['text_unit'] = textContent

					if product['unit'] == 'Lot':
						promotion['type'] = 'lot'
						promotion['selector'] = '.lineproductLine:nth-child('+unicode(2*(i+1)-1)+') a.prodimg'
						promotion['references'] = self.get_references(product['url'])
					else:
						promotion['type'] = 'simple'

				else:
					promotion['type'] = 'none'
					textContent = li.find('strong').find(text=True)
					product['price'] = float(textContent[17:-2].replace(',', '.'))

					ps = li.find('div',{'class' : 'unit price'}).find_all('p') #  p:not(.productPicto) span')[0].textContent
					if 'class' in ps[0].attrs and 'productPicto' in ps[0].attrs['class']:
						p = ps[1]
					else:
						p = ps[0]

					textContent = p.find('span').find(text=True)
					product['unit_price'] = float(textContent.split(u' € / ')[0].replace(u',', u'.'))
					product['unit'] = textContent.split(u' € / ')[1]

					textContent = p.find_all('span')[1].find(text=True)
					product['text_unit'] = textContent

				product['promotion'] = promotion
				products.append(product)
			except Exception, e:
				print 'ERROR PARSING PRODUCT : '+str(e)

		return products

	def get_references(self, url):
		references = []
		parsed_page, code = self.get_parsed_page_for_url(url)

		if code == 200:
			divs = parsed_page.find(id='ctl00_cphC_pn3T1_ctl01_pDetLot').find_all('div',{'class': 'extraProduit'})
			for div in divs:
				image = div.find('div', {'class': 'unit'}).find('a').find('img')
				reference = image.attrs['src'].split('/')[-1].split('.')[0]
				references.append(reference)
		else:
			print 'Page accession aborted'

		return references

	def __do_PostBack(self, eventTarget, eventArgument, form_parsed, cookie = "xtvrn=$460644$; vuidck=6b124715-62fb-4903-bc7b-fa8994716724; SupportCookies=true; atgPlatoStop=1; OOshopSessionState=dcu0rp450bxhq5ba2dmelf55; s_cc=true; xtan460644=-; xtant460644=1; fs_nocache_guid=0EBDF3490718C0957774FA88BFE3CC97; s_sq=%5B%5BB%5D%5D; s_vi=[CS]v1|2857A04005160775-6000018360002F45[CE]; juniper=18faf872ea4792ef9af05da1b3681935"):
		values = {}
		url = self.get_base_url()+'/'+form_parsed.get("action")

		values["__EVENTTARGET"] = eventTarget
		values["__EVENTARGUMENT"] = eventArgument
		values["__LASTFOCUS"] = ""
		values["ctl00$sm"] = 'ctl00$cphC$pn3T1$ctl01$upPaginationH|'+eventTarget

		print "Posting data to "+url

		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		req.add_header('cookie',cookie)
		response = urllib2.urlopen(req)
		
		page = response.read()
		print "Response fetched"
		parsed_page = BeautifulSoup(page,"lxml",from_encoding = 'utf-8')

		return parsed_page

def perform():
	ooshop = Ooshop()
	# ooshop.get_menu()
	# cookie = "cf=1; xtvrn="
	url = 'http://www.ooshop.com/courses-en-ligne/ContentNavigation.aspx?TO_NOEUD_IDMO=N000000013580&TO_NOEUD_IDFO=81517&NOEUD_NIVEAU=3'
	products = ooshop.get_product_list_for_url_category(url)
	print products

