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
		parsed_page = self.get_parsed_page_for_url("http://www.telemarket.fr/dynv6/index.shtml")
		# print parsed_page.prettify()
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
			parsed_page = self.get_parsed_page_for_url(url)
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

		self.set_categories(categories)


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
				print len(second_categories)
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