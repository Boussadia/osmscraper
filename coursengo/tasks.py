#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings

from apps.scrapers.coursengo import Coursengo
from models import *

coursengo = Coursengo()

def save_categories(categories):
	"""
		Saving categories in database.

		Input:
			- categories : dictionnary corresponding to the exit of coursengo scraper, containing architecture of categories and sub categories.
		Return:
			- sub_categories_final_list : list of database entity of final categories saved

	"""

	sub_categories_final_list = []

	for name_category, category_dict in categories.iteritems():
		print "Saving Main Category "+name_category
		url_category = category_dict["url"]
		category, created = Category_main.objects.get_or_create(name=name_category, defaults={"url":url_category})
		sub_categories = category_dict["sub_categories"]

		for name_sub_category, sub_category_dict in sub_categories.iteritems():
			print "Saving Sub Category Level 1 "+name_sub_category
			url_sub_category = sub_category_dict["url"]
			sub_category , created = Category_sub_level_1.objects.get_or_create(name=name_sub_category, parent_category = category, defaults={"url":url_sub_category,})
			sub_categories_final = sub_category_dict["sub_categories"]

			# for name_sub_category_level_2, sub_category_level_2_dict in sub_categories_level_2.iteritems():
			# 	print "Saving Sub Category Level 2 "+name_sub_category_level_2
			# 	url_sub_category_level_2 = sub_category_level_2_dict["url"]
			# 	sub_category_level_2, created = Category_sub_level_2.objects.get_or_create(name=name_sub_category_level_2, parent_category=sub_category, defaults={"url":url_sub_category_level_2,})
			# 	print url_sub_category_level_2
			# 	sub_categories_final = sub_category_level_2_dict["sub_categories"]

			if len(sub_categories_final)>0:
				for name_sub_category_final, sub_category_final_dict in sub_categories_final.iteritems():
					print "Saving Sub Category Final "+name_sub_category_final
					url_sub_category_final = sub_category_final_dict["url"]
					sub_category_final, created = Category_final.objects.get_or_create(name=name_sub_category_final, parent_category=sub_category, defaults={"url":url_sub_category_final,})
					sub_categories_final_list.append(sub_category_final)
			else:
				# No sub categories for sub category level 2, creating final category equal to sub category level 2
				print "Saving Sub Category Final "+name_sub_category_level_2
				sub_category_final, created = Category_final.objects.get_or_create(name=name_sub_category_level_2, parent_category=sub_category, defaults={"url":url_sub_category_level_1,})
				sub_categories_final_list.append(sub_category_final)

	return sub_categories_final_list

def get_product_list(sub_categories_final_list):
	"""
		Controls process of products fetching and saving.

		Input :
			- sub_categories_final_list : list of database entity of final categories saved (correcponding to return of save_categories)
		Return :
			Nothing
	"""

	for i in xrange(0, len(sub_categories_final_list)):
		sub_category_final = sub_categories_final_list[i]
		url_products = sub_category_final.url
		product_list = extract_products(url_products)

		# Going threw every product and saving it
		for title_product, product_dict in product_list.iteritems():
			# First we retrive information about product
			product = coursengo.extract_product(product_dict["url"])
			save_product(product, sub_category_final)
		

def extract_products(url):
	"""
		Fetches produts list from url and parses it.

		Input : 
			- url : string of the url of the produts page

		Return :
			- products : list of dictionnaries to save.
	"""
	return coursengo.extract_product_list(url)

def save_product(product, sub_category_final):
	"""
		Saves produt to database.

		Input : 
			- product : dictionnary representing product to save
			- sub_category_final : database entity of parent category
		Return :
			Nothing
	"""

	if product["status"] == 200:
		# Saving brand
		brand = save_brand(product["brand"])

		# Saving Unit
		unit = save_unit(product["unit"])

		title = product["title"]
		url = product["url"].split(";jsessionid")[0]
		price = product["price"]
		unit_price = product["unit_price"]
		image_url = product["image_url"]
		promotion = product["promotion"]

		product_db, created = Product.objects.get_or_create(title = unicode(title), url = unicode(url), category=sub_category_final, defaults={"price":price, "brand":brand, "unit":unit, "unit_price":unit_price, "image_url":unicode(image_url), "promotion":promotion })
		print "saving product "+title
		if not created:
			if product_db.title != unicode(title) or product_db.category != sub_category_final or product_db.brand != brand or product_db.price != price or product_db.unit_price != unit_price or product_db.unit != unit or product_db.image_url != unicode(image_url) or product_db.promotion != promotion:
				print "Product changed, saving again"
				product_db.title = unicode(title)
				product_db.category = sub_category_final
				product_db.brand = brand
				product_db.price = price
				product_db.unit_price = unit_price
				product_db.unit = unit
				product_db.image_url = unicode(image_url)
				product_db.promotion = promotion
				product_db.save()
			else:
				print "Product did not change"

	elif product["status"] == 404:
		print "Product not found, removing if exists in database"
		if Product.objects.filter(url=product["url"]).exists():
			Product.objects.get(url=product["url"]).delete()
	else:
		print "Aborting product saving because of error while fetching data"
	
	

def save_brand(brand_name):
	"""
		Saves brand in database.

		Input :
			- brand_name : name of the brand to save

		Return :
			- brand : database entity of the associated brand
	"""
	print "Saving brand "+ brand_name+" to database..."
	brand, created_brand = Brand.objects.get_or_create(name = unicode(brand_name))
	return brand

def save_unit(unit_name):
	"""
		Saves unit in database.

		Input :
			- unit_name : name of the unit to save

		Return :
			- unit : database entity of the associated unit
	"""
	print "Saving Unit "+ unit_name+" to database..."
	unit, created_unit = Unit.objects.get_or_create(name = unicode(unit_name))
	return unit