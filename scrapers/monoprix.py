#!/usr/bin/python
# -*- coding: utf-8 -*-

from osmscraper import OSMScraper

class Monoprix(OSMScraper):
	"""
		Scraper for monoprix.fr.
	"""

	def __init__(self):
		super(Monoprix, self).__init__("http://courses.monoprix.fr")

	def get_menu(self):
		categories = {}
		parsed_page = self.get_parsed_page_for_url("http://courses.monoprix.fr/magasin-en-ligne/courses-en-ligne.html?ok")

		menu_li = parsed_page.find(id="h_n-1").find_all("li")

		# Getting main categories
		for li in menu_li:
			class_li = li.get("class")
			title = li.find("a").get("title")
			# url = li.find("a").get("href").split(";")[0]
			url = li.find("a").get("href")
			if ('Reverse' not in class_li) and title != "MODE":
				print "Found main category : "+title
				categories[title] = {
					"url":url,
					"sub_categories": {}
				}

		# Getting sub categories
		for title in categories:
			category = categories[title]
			parsed_page = self.get_parsed_page_for_url(category["url"])
			sub_categories_html = parsed_page.find("ul",{"class","SideNav"}).find("li",{"class","Active"}).find("ul").find_all("li")

			sub_categories = {}
			for i in xrange(0,len(sub_categories_html)):
				sub_category_html = sub_categories_html[i]
				title_sub_category = sub_category_html.find("a").get("title")
				url_sub_category = sub_category_html.find("a").get("href")
				print "Found sub category : "+title_sub_category
				sub_categories[title_sub_category] ={
					"url": url_sub_category,
					"sub_categories": {}
				}

			categories[title]["sub_categories"] = sub_categories

		# Getting sub categories level 2
		for title in categories:
			category = categories[title]
			sub_categories = category["sub_categories"]

			for title_sub_category in sub_categories:
				sub_category = sub_categories[title_sub_category]
				url_sub_category = sub_category["url"]
				sub_categories_level_2 = {}
				parsed_page = self.get_parsed_page_for_url(url_sub_category)
				sub_categories_level_2_html = parsed_page.find(id="topNavigation").find("ul",{"class","N3"})
				lis = sub_categories_level_2_html.find_all("li")
				for i in xrange(0,len(lis)):
					li = lis[i]
					title_sub_category_level_2 = li.find("a").get("title")
					url_sub_category_level_2 = li.find("a").get("href")
					print "Found sub category level 2 "+title_sub_category_level_2
					sub_categories_level_2[title_sub_category_level_2] = {
						"url": url_sub_category_level_2,
						"sub_categories": {}

					}
				sub_categories[title_sub_category]["sub_categories"] = sub_categories_level_2

			category["sub_categories"] = sub_categories


		# Getting sub categories level 3
		for title in categories:
			category = categories[title]
			sub_categories = category["sub_categories"]

			for title_sub_category in sub_categories:
				sub_category = sub_categories[title_sub_category]
				sub_categories_level_2 = sub_category["sub_categories"]

				for title_sub_category_level_2 in sub_categories_level_2:
					sub_category_level_2 = sub_categories_level_2[title_sub_category_level_2]
					url_sub_category_level_2 = sub_category_level_2["url"]
					sub_category_level_3 = {}
					parsed_page = self.get_parsed_page_for_url(url_sub_category_level_2)
					ul = parsed_page.find(id="topNavigation").find("ul",{"class","N4"})
					if ul  is not None:
						lis = ul.find_all("li")

						for i in xrange(0,len(lis)):
							li = lis[i]
							title_sub_category_level_3 = li.find("a").get("title")
							url_sub_category_level_3 = li.find("a").get("href")
							print "Found sub category level 3 "+title_sub_category_level_3
							sub_category_level_3[title_sub_category_level_3] = {
								"url": url_sub_category_level_3,
							}

					sub_categories[title_sub_category]["sub_categories"][title_sub_category_level_2]["sub_categories"] = sub_category_level_3

			categories[title]["sub_categories"] = sub_categories

		self.set_categories(categories)

	def  extract_product_list(self, url):
		products ={}
		parsed_page = self.get_parsed_page_for_url(url)

		# Determining if all the products are in the page, otherwise, fetch proper page
		active_pagination = parsed_page.find("div", {"class","PageViewControl"}).find("li",{"class":"Active"}).find(text=True)
		if active_pagination != "Tous":
			print "Fetching complete product lists"
			url_all_products = ""
			links = parsed_page.find("div", {"class","PageViewControl"}).find_all("a")
			for link in links:
				if link.get("title") == "Tous":
					url_all_products = link.get("href")
					break
			parsed_page =  self.get_parsed_page_for_url(url_all_products)
		else:
			print "All products already here"

		# Extracting links to product pages
		rows_html = parsed_page.find("table",{"class":"t-data-grid"}).find_all("td",{"class","descriptionCourtePanier"})
		products = {}

		for row in rows_html:
			for child in row.findChildren(recursive=False):
				if child.name == "li":
					url_product = child.findChildren(recursive=False)[0].get("href")
					title_product = child.findChildren(recursive=False)[0].find("img").get("alt")
					print title_product
					products[title_product] ={
						"title": title_product,
						"url": url_product
					}

		return products

	def extract_product(self, url_product):
		product = {}
		parsed_page = self.get_parsed_page_for_url(url_product)
		product_section = parsed_page.find(id="ficheProduit")
		product_infos = product_section.find("div",{"class","InfoProduit"})

		product["brand"] = self.strip_string(product_infos.find("p",{"class":"Style01"}).find(text=True))
		product["title"] = self.strip_string(product_infos.find("p",{"class":"Style02"}).find(text=True))
		product["price"] = self.convert_price_to_float(product_section.find("p",{"class","priceBox"}).find("label").find(text=True))
		product["unit_price"], product["unit"] = self.strip_string(product_section.find("p",{"class":"Style06"}).find(text=True)).split(" / ")
		product["unit_price"] = self.convert_price_to_float(product["unit_price"])

		product["image_url"] = product_section.find("div",{"class","InfoProduitExtra"}).find("div",{"class","ContentCenterSubWrap"}).find("img").get("src")

		lis = product_section.find("ul",{"class","Accordion02"}).find_all("li")

		for i in xrange(0,len(lis)):
			li = lis[i]
			product[li.find("h4").find(text=True)] = li.find("p",{"class","Para04"}).find(text=True)

		return product

		