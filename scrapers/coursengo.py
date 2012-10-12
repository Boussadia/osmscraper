#!/usr/bin/python
# -*- coding: utf-8 -*-

from osmscraper import OSMScraper

import urllib
import urllib2

from bs4 import BeautifulSoup

import re

class Coursengo(OSMScraper):
	"""
		Coursengo.com scraper.
	"""
	def __init__(self):
		super(Coursengo, self).__init__("http://www.coursengo.com")

	def pre_processing_url(self, url):
		if len(url)>1 and url[0:2] == "..":
			url = url[2:]
		elif len(url)>0 and url[0] == ".":
			url = "supermarche"+url[1:]
		return url

	def get_menu(self):
		categories = {}
		parsed_page, code = self.get_parsed_page_for_url()

		if code == 200:
			# The request was sucessfull
			# Getting main categories
			lis = parsed_page.find(id="menu_univers").find_all("li",{"class","univers"})
			print "Found "+str(len(lis))+" main categories."
			for i in xrange(1,len(lis)):
				li = lis[i]
				children = li.findChildren(recursive=False)
				title = ""
				for j in xrange(0,len(children)):
					child = children[j]
					if child.name == "a":
						title = child.find(text=True)
						url = self.pre_processing_url(child.get("href"))
						break

				print "Found main category "+title
				categories[title] = {
					"sub_categories": {},
					"url": url
				}

			# Getting sub categories level 1
			for title, category in categories.iteritems():
				sub_categories_level_1 = {}
				parsed_page, code = self.get_parsed_page_for_url(category["url"])
				if code == 200:
					# The request was sucessfull
					lis = parsed_page.find(id="menuNavUnivers").find("div",{"class","menugauche"}).find_all("li")
					print "Found "+str(len(lis))+" sub categories level 1."
					for i in xrange(0, len(lis)):
						li = lis[i]
						a = li.find("a")
						print "Found sub category level 1 "+a.find(text=True)+" for main category "+title
						sub_categories_level_1[a.find(text=True)] = {
							"url": self.pre_processing_url(a.get("href")),
							"sub_categories": {}
						}
					categories[title]["sub_categories"] = sub_categories_level_1
				else:
					print"Aborting scraping of sub categories level 1."

			# Getting sub categories level 2
			for title, category in categories.iteritems():
				sub_categories_level_1 = category["sub_categories"]

				for title_sub_category_level_1, sub_category_level_1 in sub_categories_level_1.iteritems():
					sub_categories_level_2 = {}
					parsed_page, code = self.get_parsed_page_for_url(sub_category_level_1["url"])

					if code == 200:
						# The request was sucessfull
						lis = parsed_page.find(id="menuNavUnivers").find("div",{"class","menugauche"}).find("li",{"class","active"}).find_all("li")
						print "Found "+str(len(lis))+" sub categories level 2."
						for i in xrange(0, len(lis)):
							a = lis[i].find("a")
							print "Found sub category level 2 "+a.find(text=True)+" for sub category level 1 "+title_sub_category_level_1
							sub_categories_level_2[a.find(text=True)] = {
								"url": self.pre_processing_url(a.get("href")),
							}
						categories[title]["sub_categories"][title_sub_category_level_1]["sub_categories"] = sub_categories_level_2
					else:
						print"Aborting scraping of sub categories level 2."

			self.set_categories(categories)
		else:
			print "Aborting scraping of main categories."

	def extract_product_lists(self, url):
		"""
			Extracting product list for a sub category page

			Input :
				- url : url of sub category
			Return :
				- products : dictionnary of products list with name and link to product page
		"""
		products = {}
		parsed_page, code = self.get_parsed_page_for_url(url)

		if code == 200:
			# The request was sucessfull
			# Getting page of all products, requires a POST with certain variables that we need to extract for page:
			CTX_value = parsed_page.find(id="colcentre").find("form").find("input").get("value")
			# Performing POST and retrieving resulting page
			parsed_page = self.retrieve_parsed_page_all_products(CTX_value)
			produtcs_html = parsed_page.find_all("div",{"class","simple"})

			for i in xrange(0,len(produtcs_html)):
				url_product = self.pre_processing_url(produtcs_html[i].find("div",{"class","img"}).find("a").get("href"))
				title_product = produtcs_html[i].find("div",{"class","img"}).find("a").find("img").get("alt")[9:-9]

				products[title_product] = {
					"url": url_product
				}
		else:
			print "Aborting scraping of products list."

	def extract_product(self,url):
		product = {}
		parsed_page, code = self.get_parsed_page_for_url(url)
		product["url"] = url
		product["code"] = code

		if code == 200:
			# The request was sucessfull
			fiches_produit = parsed_page.find_all("div",{"class":"ficheproduit"})
			for i in xrange(0,len(fiches_produit)):
				fiche = fiches_produit[i]
				form = fiche.find("form")
				if form is not None:
					url_image = form.find("div",{"class","img"}).find("img").get("src")
					price = self.convert_price_to_float(form.find("div",{"class","blocprix"}).find("div",{"class","prix"}).find(text=True))
					brand = form.find("div",{"class","texte"}).find("h1").find(text=True)
					title = form.find("div",{"class","texte"}).find("h2").find(text=True).split(" - ")[0]
					quantity_text = form.find("div",{"class","texte"}).find("h2").find(text=True).split(" - ")[-1]

					# Unit and unit price
					unit_html = form.find("div",{"class","texte"}).find("span").find(text=True)
					if unit_html is None:
						unit = "Unit"
						if re.match(r"(\d)+",quantity_text):
							quantity = self.convert_price_to_float(re.match(r"(\d)+",quantity_text).group())
							unit_price = price / quantity
						else:
							unit_price = -1
					else:
						unit_price, unit = unit_html.split(" / ")
						unit_price = self.convert_price_to_float(unit_price)

					# Promotion
					promotion_html = form.find("div",{"class","blocprix"}).find("div",{"class","prix"}).find("span")
					if promotion_html is not None:
						promotion =  1- price / self.convert_price_to_float(promotion_html.find(text=True))
						print promotion
					else:
						promotion = 0

					product["title"] = title
					product["url_image"] = url_image
					product["price"] = price
					product["brand"] = brand
					product["quantity_text"] = quantity_text
					product["unit"] = unit
					product["unit_price"] = unit_price
					product["promotion"] = promotion

		else:
			print "Aborting scraping of product."

		return product



	def retrieve_parsed_page_all_products(self, CTX_value):
		url = "http://www.coursengo.com/supermarche/univers.html"
		values = {
			'CTX': CTX_value,
			'EVT':'FORM_ACTION=S:FILTRER_NB_PRODUIT_PAR_PAGE',
			'ZZDTO_SORT_LISTE_PRODUITXXRECH_SORT_NB_PAGE_ID': 4
		}

		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
		response.close()
		parsed_page = BeautifulSoup(the_page, "lxml")
		return parsed_page