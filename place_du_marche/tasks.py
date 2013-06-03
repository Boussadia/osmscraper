#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings

from apps.scrapers.place_du_marche import Place_du_marche
from models import *

place_du_marche = Place_du_marche()

def save_categories(categories):
	# Firt we extract main categories from dictonary
	categories_final_objects = []


	for name_category in categories:
		print "Saving category "+name_category+" to database"
		category, created = Category_main.objects.get_or_create(name = name_category)

		categories_sub = {name_category_sub: {"url": categories[name_category][name_category_sub]["url"]} for name_category_sub in categories[name_category] }
		
		categories_sub_objects = save_categories_sub_for_main( categories_sub = categories_sub, category_main= category)

		for category_sub_object in categories_sub_objects:
			category_sub = categories[name_category][category_sub_object.name]
			nb_final_categories = len(category_sub["sub_categories"])

			if nb_final_categories == 0:
				print "Saving final category "+category_sub_object.name+" to database"
				category_final_objects, created = Category_final.objects.get_or_create(name = category_sub_object.name, parent_category = category_sub_object, url= category_sub_object.url)
				categories_final_objects.append(category_final_objects)
			else:
				categories_final = category_sub["sub_categories"]
				categories_final_objects = categories_final_objects + save_categories_final_for_sub(categories_final = categories_final,  category_sub = category_sub_object)

	return categories_final_objects


def save_categories_sub_for_main(categories_sub, category_main):
	categories_objects = []
	for name_category_sub in categories_sub:
		url_category_sub = categories_sub[name_category_sub]['url']
		print "Saving sub category "+ unicode(name_category_sub)+" to database"
		category_sub, created = Category_sub.objects.get_or_create(name = unicode(name_category_sub), parent_category = category_main, url= url_category_sub)
		categories_objects.append(category_sub)

	return categories_objects

def save_categories_final_for_sub(categories_final, category_sub):
	categories_final_objects = []
	for name_category_final in categories_final:
		url_category_final = categories_final[name_category_final]['url']
		print "Saving final category "+ unicode(name_category_final)+" to database"
		category_final, created = Category_final.objects.get_or_create(name = unicode(name_category_final), parent_category = category_sub, url= url_category_final)
		categories_final_objects.append(category_final)

	return categories_final_objects


def perform_scraping():
	place_du_marche.get_menu()
	categories = place_du_marche.get_categories()
	categories_final = save_categories(categories)

	for i in xrange(0, len(categories_final)):
		category_final = categories_final[i]
		products = place_du_marche.extract_product_list(category_final.url)
		for product_key in products:
			product = products[product_key]

			if product["status"] == 200:
				# Product retrieved successfully
				url = product_key
				print "Url product : "+url
				title = product["title"]
				brand_str = product["brand"]
				print "Saving brand "+ brand_str+" to database..."
				brand, created_brand = Brand.objects.get_or_create(name = brand_str)
				full_text = product["full_text"]

				price = product["price"]
				unit_price = product["unit_price"]
				unit_str = product["unit"]
				print "Saving unit "+ unit_str+" to database..."
				unit, created_unit = Unit.objects.get_or_create(name = unit_str)
				image_url = product["image_url"]
				promotion = product["promotion"]

				print "Saving product "+ title+" to database..."
				product_object, created = Product.objects.get_or_create(category = category_final ,title = unicode(title),  url= unicode(url), defaults= { "brand" : brand, "full_text" : unicode(full_text), "price" : price, "unit_price" : unit_price, "unit" : unit, "image_url" : unicode(image_url), "promotion" : promotion})

				if not created:
					if product_object.title != unicode(title) or product_object.category != category_final or product_object.brand != brand or product_object.full_text != unicode(full_text) or product_object.price != price or product_object.unit_price != unit_price or product_object.unit != unit or product_object.image_url != unicode(image_url) or product_object.promotion != promotion:
						print "Product changed, saving again"
						product_object.title = unicode(title)
						product_object.category = category_final
						product_object.brand = brand
						product_object.full_text = unicode(full_text)
						product_object.price = price
						product_object.unit_price = unit_price
						product_object.unit = unit
						product_object.image_url = unicode(image_url)
						product_object.promotion = promotion
						product_object.save()
					else:
						print "Product did not change"
			elif product["status"] == 404:
				print "Product not found, removing if exists in database"
				if Product.objects.filter(url=product_key).exists():
					Product.objects.get(url=product_key).delete()

# print place_du_marche.extract_product("http://www.placedumarche.fr/supermarche-en-ligne-livraison-tendre-noix-la-broche-2-1-tranche-gratuite,10179,4,182,1001.htm")
