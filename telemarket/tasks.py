#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import connection

from scrapers.telemarket import Telemarket
from models import *

from osmscraper.utility import dictfetchall

telemarket = Telemarket()

def save_categories(categories):
	# Firt we extract main categories from dictonary
	categories_final_objects = []


	for name_category in categories:
		print "Saving category "+name_category+" to database"
		url_category = categories[name_category]["url"]
		category, created = Category_main.objects.get_or_create(name = unicode(name_category), url = unicode(url_category))

		sub_categories = categories[name_category]["sub_categories"]

		for name_category_sub in sub_categories:
			print "Saving sub category "+name_category_sub+" to database"
			sub_category, sub_created = Category_sub_1.objects.get_or_create(name = unicode(name_category_sub), parent_category = category)
			for name_category_sub_lvl_2 in sub_categories[name_category_sub]:
				print "Saving sub category level 2 "+name_category_sub_lvl_2+" to database"
				url_sub_categories_lvl_2 = sub_categories[name_category_sub][name_category_sub_lvl_2]["url"]
				sub_category_lvl_2, sub_created = Category_sub_2.objects.get_or_create(name = unicode(name_category_sub_lvl_2), url = unicode(url_sub_categories_lvl_2), parent_category = sub_category)

				if len(sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"]) == 0:
					sub_category_lvl_3, sub_created = Category_sub_3.objects.get_or_create(name = unicode(name_category_sub_lvl_2), url = unicode(url_sub_categories_lvl_2), parent_category = sub_category_lvl_2)
					sub_category_lvl_4, sub_created = Category_final.objects.get_or_create(name = unicode(name_category_sub_lvl_2), url = unicode(url_sub_categories_lvl_2), parent_category = sub_category_lvl_3)
					save_products(url_sub_categories_lvl_2, sub_category_lvl_4)
				else:
					for name_category_sub_lvl_3 in sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"]:
						print "Saving sub category level 3 "+name_category_sub_lvl_3+" to database"
						url_sub_categories_lvl_3 = sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"][name_category_sub_lvl_3]["url"]
						sub_category_lvl_3, sub_created = Category_sub_3.objects.get_or_create(name = unicode(name_category_sub_lvl_3), url = unicode(url_sub_categories_lvl_3), parent_category = sub_category_lvl_2)
						
						if len(sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"][name_category_sub_lvl_3]["sub_categories"]) == 0:
							sub_category_lvl_4, sub_created = Category_final.objects.get_or_create(name = unicode(name_category_sub_lvl_3), url = unicode(url_sub_categories_lvl_3), parent_category = sub_category_lvl_3)
							save_products(url_sub_categories_lvl_3, sub_category_lvl_4)
						else:
							for name_category_sub_lvl_4 in sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"][name_category_sub_lvl_3]["sub_categories"]:
								print "Saving sub category level 4 "+name_category_sub_lvl_4+" to database"
								url_sub_categories_lvl_4 = sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"][name_category_sub_lvl_3]["sub_categories"][name_category_sub_lvl_4]["url"]
								sub_category_lvl_4, sub_created = Category_final.objects.get_or_create(name = unicode(name_category_sub_lvl_4), url = unicode(url_sub_categories_lvl_4), parent_category = sub_category_lvl_3)
								save_products(url_sub_categories_lvl_4, sub_category_lvl_4)
	return categories_final_objects

def save_products(url_sub_category, category_final):
	products = telemarket.extract_product_list(url_sub_category)

	for product_name in products:
		product = products[product_name]
		title = product["title"]
		url = product["url"]
		reference = product['reference']
		price = product["price"]
		unit_str = product["unit"]
		unit_price = product["unit_price"]
		image_url = product["image_url"]
		promotion_bool = product["promotion"]
		type_promotion = product["type_promotion"]

		# Promotion
		promotion, created_promotion = Promotion.objects.get_or_create(type= unicode(type_promotion))

		# Unit
		unit, created_unit = Unit.objects.get_or_create(name = unit_str)

		product_object, created = Product.objects.get_or_create(reference = unicode(reference), defaults= {"category": category_final, "title": unicode(title), "url": unicode(url),"price" : price, "unit_price" : unit_price, "unit" : unit, "image_url" : unicode(image_url), "promotion" : promotion})

		if created:
			print "Saving new product "+ title+" to database..."
		else:
			print "Updating product "+ title+" to database..."

		history = Product_history(telemarket_product = product_object, price = price, unit_price=unit_price, unit= unit, promotion=promotion)
		history.save()

def perform_scraping():
	telemarket.get_menu()
	categories = telemarket.get_categories()
	save_categories(categories)

def set_references():
	products = Product.objects.all()
	for product in products:
		url = product.url
		reference = url.split('/')[-1].split('-')[0]
		print reference
		product.reference = reference
		product.save()

def set_unique_products():
	sql_query = ("SELECT COUNT(*)/2 AS count, t1.reference AS reference "
					"FROM telemarket_product AS t1, telemarket_product AS t2 "
					"WHERE t1.id <> t2.id AND t1.reference = t2.reference "
					"GROUP BY t1.reference ORDER BY t1.reference ASC ;");
	cursor = connection.cursor()
	cursor.execute(sql_query)
	result_db = dictfetchall(cursor)
	for i in xrange(0, len(result_db)):
		reference = result_db[i]['reference']
		products = Product.objects.filter(reference = reference)
		product_to_save = products[0]
		for product in products:
			if product.monoprix_product_id is not None:
				product_to_save.monoprix_product_id = product.monoprix_product_id
			product.delete()
		product_to_save.save()

def set_history():
	products = Product.objects.all()

	for product in products:
		price = product.price
		unit_price = product.unit_price
		unit = product.unit
		promotion = product.promotion
		history = Product_history(telemarket_product = product, price = price, unit_price=unit_price, unit= unit, promotion=promotion)
		history.save()
		print history
