#!/usr/bin/python
# -*- coding: utf-8 -*-

from osmscraper import OSMScraper

class Place_du_marche(OSMScraper):
	"""
	"""

	def __init__(self):
		super(Place_du_marche, self).__init__("http://www.placedumarche.fr")

	def get_menu(self):
		categories = {}
		parsed_page, code = self.get_parsed_page_for_url()

		if code == 200:
			# The request was sucessfull
			menu = parsed_page.find(id="menu").find_all("td")

			print "Found "+str(len(menu))+" main categories."

			for i in xrange(len(menu)):
				title = menu[i].find_all("a")[0].get("title")[:-54]
				print "Working on category "+title
				categories[title] = {}
				sub_menus = menu[i].find_all("ul")[0]
				sub_category = {}
				for child in sub_menus.children:
					a = child.find("a")
					if a != -1:
						title_sub_catagory = a.find(text=True)
						print "Found sub category "+title_sub_catagory+" for "+title

						url = a.get("href")
						sub_category[title_sub_catagory] = {
							"url": self.get_base_url()+ "/" +url,
							"sub_categories": {}
						}
					sub_childs = child.find("ol")

					if sub_childs is not None and sub_childs != -1:
						last_sub_category = {}
						for a in sub_childs.findAll("a"):
							titre_sub_child_a = a.find(text=True)
							url_last_child = self.get_base_url()+ "/" + a.get("href")
							if titre_sub_child_a != "Tout afficher":
								print "Found last catagory "+titre_sub_child_a+" for sub category "+title_sub_catagory
								last_sub_category[titre_sub_child_a] = {}
								last_sub_category[titre_sub_child_a]["url"] = url_last_child

						sub_category[title_sub_catagory]["sub_categories"] = last_sub_category

				categories[title] = sub_category

			self.set_categories(categories)
		else:
			print "Aborting scraping of main categories."

	def get_products(self):
		categories = self.get_categories()
		for key_category in categories:
			category = categories[key_category]
			print "Extracting produt list for main category "+key_category
			for key_sub_category in category:
				sub_category = category[key_sub_category]
				url = sub_category["url"]
				sub_category_level_2 = sub_category["sub_categories"]
				print "Extracting produt list for sub category "+key_sub_category

				if len(sub_category_level_2) == 0:
					print "Extracting for category "+key_sub_category
					products = self.extract_product_list(url)
					sub_category["products"] = products
				else:
					for key_last_level in sub_category_level_2:
						print "Extracting for category "+key_last_level
						products = self.extract_product_list(sub_category_level_2[key_last_level]["url"])
						sub_category_level_2[key_last_level]["products"] = products
					sub_category["sub_categories"] = sub_category_level_2
				category[key_sub_category] = sub_category
			categories[key_category] = category

	def extract_product_list(self, url):
		products = {}
		parsed_page, code = self.get_parsed_page_for_url(url)

		if code == 200:
			# The request was sucessfull
			center = parsed_page.find("center")
			if center is not None:
				product_list = center.find_all("td",{"class":"produitTd"})
				print "Found "+str(len(product_list))+" products"

				for product in product_list:
					html_product = product.find(id="libelle").find_all("h4")[0].find("a")
					url_product = html_product.get("href")
					products[url_product] = self.extract_product(url_product)
		else:
			print "Aborting products list scraping"

		return products

	def extract_product(self, url):
		product = {
			"status": 200,
			"url": url
		}
		image_url = ""
		promotion = 0 # Sometimes promotion price = normal price, reason : same price but more of the product => -1 = no promotion for sure, else promotion
		title_product = ""
		price = 0
		unit_price = 0
		unit = ""
		brand = ""
		block_text = ""

		parsed_page, code = self.get_parsed_page_for_url(url)
		product["status"] = code

		if code == 200:
			# The request was sucessfull
			product_html = parsed_page.find(id="produit")

			# Getting image url
			if product_html is not None:
				image_html = product_html.findAll("table",{"class": "photoInner"})
				if len(image_html)>0:
					image_html = image_html[0]
					image_url = image_html.find("img").get("src")
				
				# Getting title
				infos_produits_html = product_html.find(id="infosProduit")
				if infos_produits_html is not None:
					title_product = infos_produits_html.find(id="libelleProd")
					if title_product is not None:
						title_product = title_product.find(text=True)

				# Getting price
				
				if infos_produits_html is not None:
					price_html = infos_produits_html.findAll("div", {"class": "prix"} )
					if len(price_html)>0:
						if price_html[0].find("strike") is not None:
							price = self.convert_price_to_float(price_html[0].find("strike").find(text=True)[:-2])
							price_after_promotion = self.convert_price_to_float(price_html[0].find("strong").find(text=True)[:-2])
							promotion = 1- price_after_promotion/price 
						else:
							price = self.convert_price_to_float(price_html[0].find("strong").find(text=True)[:-6])
							promotion = -1 
				

				# Getting unit price
				if infos_produits_html is not None:
					price_text = infos_produits_html.findAll("div", {"class": "prix"} )
					if len(price_text)>0:
						if len(price_text[0].findAll(text=True))>0:
							if len(price_text[0].findAll(text=True)[-1].split())>0:
								if promotion != -1:
									if len(price_text[0].findAll(text=True)[-1].split())>1:
										unit_price = self.convert_price_to_float(price_text[0].findAll(text=True)[-1].split()[1][1:])
										unit = price_text[0].findAll(text=True)[-1].split()[-1][:-1]
									else:
										unit_price = -1
										unit = "Unit"
								else:
									if len(price_text[0].findAll(text=True)[-1].split())>0:
										unit_price = self.convert_price_to_float(price_text[0].findAll(text=True)[-1].split()[0][1:])
										unit = price_text[0].findAll(text=True)[-1].split()[-1][:-1]
									else:
										unit_price = -1
										unit = "Unit"
							else:
								unit_price = -1
								unit = "Unit"


				# Getting Brand
				
				block_detail = product_html.findAll("div",{"class", "blockInfo"})
				
				
				for block in block_detail:
					if block.find(id="sousLibelleProd") is not None:
						if block.find(id="sousLibelleProd").find(text=True) == "Détails :".decode("utf-8"):
							block = block.findAll("div",{"class", "texte"})
							if len(block)>0:
								block = block[0].findAll("p")
								if len(block)>0:
									block = block[0].find(text=True)
									block_text = block
									if block is not None:
										block = block.split(" ")
										if len(block)>0:
											brand = block[0]
			
			
			product["price"] = price
			product["unit_price"] = unit_price
			product["unit"] = unit
			product["title"] = title_product
			product["promotion"] = promotion
			product["image_url"] = image_url	
			product["brand"] = brand
			product["full_text"] = block_text

		else:
			print "Aborting scraping of product"

		return product