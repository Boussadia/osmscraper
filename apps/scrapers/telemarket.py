#!/usr/bin/python
# -*- coding: utf-8 -*-

from osmscraper import OSMScraper

class Telemarket(OSMScraper):
	"""
		Scrapper for telemarket.fr
	"""

	def __init__(self):
		super(Telemarket, self).__init__("http://www.telemarket.fr")

	def get_menu(self):
		categories = {}
		parsed_page, code = self.get_parsed_page_for_url("http://www.telemarket.fr/dynv6/index.shtml")

		if code == 200:
			# The request was sucessfull
			menu_html = parsed_page.find(id="menuP").find_all("ul",{"class":"first"})[0]
			categories_html = menu_html.find_all("li")

			# Site menu nb : index 0 = home, we skip it is not a category
			for i in xrange(1,len(categories_html)):
				category_html = categories_html[i]
				category_name = category_html.find(text=True)
				category_url = category_html.find_all("a")[0].get("href")
				categories[category_name] = {
					"url": category_url,
				}

			for category_name in categories:
				category = categories[category_name]

				url = self.get_base_url()+category["url"]
				parsed_page, code = self.get_parsed_page_for_url(url)
				if code == 200:
					# The request was sucessfull
					left_column = parsed_page.find(id="zoneGauche")
					
					titles = left_column.find_all("div",{"class":"menuTitle"})
					sub_categories = left_column.find_all("div",{"class":"menuYaAccordeon"})
					
					category["sub_categories"] ={}

					if len(titles) == len(sub_categories):
						for i in xrange(0,len(titles)):
							sub_category_html = sub_categories[i].find("ul",{"class":"subMenuLevel1"})
							sub_category = self.extract_sub_category_level_1(sub_category_html)
							title = titles[i].find_all("strong")[0].find(text=True)
							title = " ".join(title.split())
							category["sub_categories"][title] = sub_category
							
					else:
						sub_category_html = sub_categories[0].find("ul",{"class":"subMenuLevel1"})
						sub_category = self.extract_sub_category_level_1(sub_category_html)
						category["sub_categories"][category_name] = sub_category

						second_category = self.extract_sub_category_level_2(sub_category_html)
						

					categories[category_name] = category
				else:
					print "Aborting scraping sub categories"

			self.set_categories(categories)
		else:
			print "Aborting scraping of main categories"


	def extract_sub_category_level_1(self, first_category_html):
		first_categories = {}
		for child in first_category_html.findChildren( recursive=False):
			name = child.find("span").find("a").find(text=True)
			url = child.find("span").find("a").get("href")
			first_categories[name] = {}
			first_categories[name]["url"] = url
			second_categories = self.extract_sub_category_level_2(child.find("ul",{"class":"subMenuLevel2"}))
			first_categories[name]["sub_categories"] = second_categories
		return first_categories

	def extract_sub_category_level_2(self, first_category_html):
		first_categories = {}
		if first_category_html is not None:
			for child in first_category_html.findChildren( recursive=False):
				name = child.find("span").find("a").find(text=True)
				url = child.find("span").find("a").get("href")
				first_categories[name] = {}
				first_categories[name]["url"] = url
				second_categories = self.extract_sub_category_level_3(child.find("ul",{"class":"subMenuLevel3"}))
				first_categories[name]["sub_categories"] = second_categories
		return first_categories

	def extract_sub_category_level_3(self, first_category_html):
		first_categories = {}
		if first_category_html is not None:
			for child in first_category_html.findChildren( recursive=False):
				name = child.find("span").find("a").find(text=True)
				url = child.find("span").find("a").get("href")
				first_categories[name] = {}
				first_categories[name]["url"] = url
		return first_categories


	def extract_product_list(self, url):
		products = {}
		parsed_page, code = self.get_parsed_page_for_url(url)

		if code == 200:
			# The request was sucessfull
			block_produtcs_html = parsed_page.find("div",{"class","blocListeProduit"})

			if block_produtcs_html is not None:
				product_list = block_produtcs_html.find_all("div",{"class":"blocConteneurProduit"})
				print "Found "+str(len(product_list))+" products"

				for product in product_list:
					p = self.extract_product(product)

					products[p["title"]] = p
		else:
			print "Aborting scraping products list"

		return products

	def extract_product(self, product):
		image_url = self.convert_image_url(product.find("div",{"class":"imageProduit"}).find("img").get("src"))
		title = product.find("div",{"class":"blocDescriptionProduit"}).find("span").find(text=True)
		url = product.find("div",{"class":"imageProduit"}).find("a").get("href")
		reference = url.split('/')[-1].split('-')[0]
		if product.find("div",{"class":"blocTarifProduit"}).find(text=True) is not None:
			price = self.convert_price_to_float(product.find("div",{"class":"blocTarifProduit"}).find(text=True)[:-2])
		else:
			price = -1

		unit_price_html = product.find("div",{"class":"prixPoidsProduit"}).find(text=True)
		if unit_price_html is None:
			unit = "Unit"
			unit_price = -1
		else:
			unit = unit_price_html.split(' / ')[-1]
			unit_price = self.convert_price_to_float(unit_price_html.split(' / ')[0][:-2])


		promotion = False
		type_promotion = ''
		# Promotion
		img_html = product.find("div",{"class":"infoDroiteProduit"}).find("img")
		if img_html is not None and img_html.get("alt")=="promotion":
			promotion = True
			label_promoation = product.find("div",{"class":"LabelProduitPromo"})
			if label_promoation is not None:
				type_promotion = label_promoation.find("span").find(text=True)

		return { 
					"reference": reference,
					"url": url,
					"title": title,
					"price": price,
					"unit": unit,
					"unit_price": unit_price,
					"image_url": image_url,
					"promotion": promotion,
					"type_promotion": type_promotion,
				}

	def convert_image_url(self, image_url):
		return image_url[:-6]+"t0.jpg" 