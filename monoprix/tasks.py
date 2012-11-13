#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings

from scrapers.monoprix import Monoprix
from models import *

monoprix = Monoprix()

def save_categories(categories):
	"""
		Saving categories in database.

		Input:
			- categories : dictionnary corresponding to the exit of monoprix scraper, containing architecture of categories and sub categories.
		Return:
			- sub_categories_final_list : list of database entity of final categories saved

	"""

	sub_categories_final_list = []

	for name_category in categories:
		print "Saving Main Category "+name_category
		url_category = categories[name_category]["url"]
		category, created = Category_main.objects.get_or_create(name=name_category, defaults={"url":url_category})
		sub_categories = categories[name_category]["sub_categories"]

		for name_sub_category in sub_categories:
			print "Saving Sub Category Level 1 "+name_sub_category
			url_sub_category = sub_categories[name_sub_category]["url"]
			sub_category , created = Category_sub_level_1.objects.get_or_create(name=name_sub_category, parent_category = category, defaults={"url":url_sub_category,})
			sub_categories_level_2 = sub_categories[name_sub_category]["sub_categories"]

			for name_sub_category_level_2 in sub_categories_level_2:
				print "Saving Sub Category Level 2 "+name_sub_category_level_2
				url_sub_category_level_2 = sub_categories_level_2[name_sub_category_level_2]["url"]
				sub_category_level_2, created = Category_sub_level_2.objects.get_or_create(name=name_sub_category_level_2, parent_category=sub_category, defaults={"url":url_sub_category_level_2,})
				sub_categories_final = sub_categories_level_2[name_sub_category_level_2]["sub_categories"]

				if len(sub_categories_final)>0:
					for name_sub_category_final in sub_categories_final:
						print "Saving Sub Category Final "+name_sub_category_final
						url_sub_category_final = sub_categories_final[name_sub_category_final]["url"]
						sub_category_final, created = Category_final.objects.get_or_create(name=name_sub_category_final, parent_category=sub_category_level_2, defaults={"url":url_sub_category_final,})
						sub_categories_final_list.append(sub_category_final)
				else:
					# No sub categories for sub category level 2, creating final category equal to sub category level 2
					print "Saving Sub Category Final "+name_sub_category_level_2
					sub_category_final, created = Category_final.objects.get_or_create(name=name_sub_category_level_2, parent_category=sub_category_level_2, defaults={"url":url_sub_category_level_2,})
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
		product_lists = extract_products(url_products)

		# Going threw every product and saving it
		for title_product in product_lists:
			# First we retrive information about product
			product = monoprix.extract_product(product_lists[title_product]["url"])
			save_product(product, sub_category_final)
		

def extract_products(url):
	"""
		Fetches produts list from url and parses it.

		Input : 
			- url : string of the url of the produts page

		Return :
			- products : list of dictionnaries to save.
	"""
	return monoprix.extract_product_list(url)

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
		reference = url.split('/')[-1].split('-')[-1]
		if 'LV' in reference:
			reference = reference.split('_')[1]
		price = product["price"]
		unit_price = product["unit_price"]
		image_url = product["image_url"]
		promotion = product["promotion"]

		# Optionnal fields
		description = None
		ingredients = None
		valeur_nutritionnelle = None
		conservation = None
		conseil = None
		composition = None

		if "Description" in product.keys():
			description = unicode(product["Description"])

		if "Ingr\xe9dients" in product.keys():
			ingredients = unicode(product["Ingr\xe9dients"])

		if "Valeur nutritionnelle" in product.keys():
			valeur_nutritionnelle = unicode(product["Valeur nutritionnelle"])

		if "Conservation" in product.keys():
			conservation = unicode(product["Conservation"])

		if "Composition" in product.keys():
			composition = unicode(product["Composition"])

		if "Conseil" in product.keys():
			conseil = unicode(product["Conseil"])

		product_db, created = Product.objects.get_or_create(reference = reference, defaults={"title": unicode(title), "url": unicode(url), "category":sub_category_final, "price":price, "brand":brand, "unit":unit, "unit_price":unit_price, "image_url":unicode(image_url), "promotion":promotion, "description":description, "valeur_nutritionnelle":valeur_nutritionnelle, "conservation":conservation, "composition":composition, "conseil":conseil, "ingredients":ingredients })
		print "saving product "+title
		if not created:
			if product_db.title != unicode(title) or product_db.category != sub_category_final or product_db.brand != brand or product_db.price != price or product_db.unit_price != unit_price or product_db.unit != unit or product_db.image_url != unicode(image_url) or product_db.promotion != promotion  or product_db.description != description or product_db.valeur_nutritionnelle != valeur_nutritionnelle or product_db.conservation != conservation or product_db.composition != composition or product_db.conseil != conseil or product_db.ingredients != ingredients:
				print "Product changed, saving again"
				product_db.title = unicode(title)
				product_db.category = sub_category_final
				product_db.brand = brand
				product_db.price = price
				product_db.unit_price = unit_price
				product_db.unit = unit
				product_db.image_url = unicode(image_url)
				product_db.promotion = promotion
				product_db.conseil = conseil
				product_db.conservation = conservation
				product_db.description = description
				product_db.valeur_nutritionnelle = valeur_nutritionnelle
				product_db.ingredients = ingredients
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
	brand, created_brand = Brand.objects.get_or_create(name = brand_name)
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
	unit, created_unit = Unit.objects.get_or_create(name = unit_name)
	return unit

def perform_scraping():
	monoprix.get_menu()
	categories = monoprix.get_categories()
	sub_categories_final_list = save_categories(categories)
	get_product_list(sub_categories_final_list)


def set_references():
	products = Product.objects.all()

	for product in products:
		reference = product.url.split('/')[-1].split('-')[-1]
		if 'LV' in reference:
			reference = reference.split('_')[1]
		product.reference = reference
		try:
			product.save()
		except Exception, e:
			print reference
			print e

def set_unique_references():
	from osmscraper.utility import dictfetchall
	from django.db import connection
	from telemarket.models import Product as Telemarket_product
	sql_query = ("select m.reference from (select monoprix_product.reference, count(*) as count from monoprix_product group by reference order by count desc) as m where m.count>1")
	cursor = connection.cursor()
	cursor.execute(sql_query)
	result_db = dictfetchall(cursor)
	
	for result in result_db:
		print 'Working on reference '+result['reference']
		products = Product.objects.raw("SELECT * from monoprix_product where reference = '%s'"%( result['reference']))
		product_to_save = products[0]
		telemarket_products_matching = Telemarket_product.objects.raw("select * from telemarket_product join monoprix_product on monoprix_product.id = telemarket_product.monoprix_product_id where monoprix_product.reference = '%s'"%(result['reference']))
		for match in telemarket_products_matching:
			match.monoprix_product_id = product_to_save.id
			match.save()

		for product in  products:
			product.delete()
		product_to_save.save()