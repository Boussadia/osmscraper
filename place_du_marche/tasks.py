#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.setrecursionlimit(1500)

from celery.task.schedules import crontab
from celery.task import periodic_task

from django.conf import settings
from celery import Celery

from scrapers.place_du_marche import Place_du_marche
from models import *

celery = Celery('tasks', broker=settings.BROKER_URL)
place_du_marche = Place_du_marche()

def save_categories(categories):
	# Firt we extract main categories from dictonary
	# categories_objects = []
	for name_category in categories:
		category, created = Category_main.objects.get_or_create(name = name_category)
		# categories_objects.append((category,created))

		categories_sub = {name_category_sub: {"url": categories[name_category][name_category_sub]["url"]} for name_category_sub in categories[name_category] }
		
		categories_sub_objects = save_categories_sub_for_main( categories_sub = categories_sub, category_main= category)

		for category_sub_object in categories_sub_objects:
			category_sub = categories[name_category][category_sub_object.name]
			nb_final_categories = len(category_sub["sub_categories"])

			if nb_final_categories == 0:
				Category_final.objects.get_or_create(name = category_sub_object.name, parent_category = category_sub_object, url= category_sub_object.url)
			else:
				categories_final = category_sub["sub_categories"]
				save_categories_final_for_sub(categories_final = categories_final,  category_sub = category_sub_object)


	# return categories_objects

def save_categories_sub_for_main(categories_sub, category_main):
	categories_objects = []
	for name_category_sub in categories_sub:
		url_category_sub = categories_sub[name_category_sub]['url']
		category_sub, created = Category_sub.objects.get_or_create(name = unicode(name_category_sub), parent_category = category_main, url= url_category_sub)
		categories_objects.append(category_sub)

	return categories_objects

def save_categories_final_for_sub(categories_final, category_sub):
	categories_final_objects = []
	for name_category_final in categories_final:
		url_category_final = categories_final[name_category_final]['url']
		category_final, created = Category_final.objects.get_or_create(name = unicode(name_category_final), parent_category = category_sub, url= url_category_final)
		categories_final_objects.append(category_final)

	return categories_final_objects

def save_products(products):
	print len(products)


@periodic_task(run_every=crontab(minute=0, hour=0))
def get_place_du_marche_categories():
	place_du_marche.get_menu()
	categories = place_du_marche.get_categories()
	categories_objects = save_categories(categories)

	# for key_category in categories:
	# 	category = categories[key_category]
	# 	print "Extracting produt list for main category "+key_category
	# 	for key_sub_category in category:
	# 		sub_category = category[key_sub_category]
	# 		url = sub_category["url"]
	# 		sub_category_level_2 = sub_category["sub_categories"]
	# 		print "Extracting produt list for sub category "+key_sub_category

	# 		if len(sub_category_level_2) == 0:
	# 			print "Extracting for category "+key_sub_category
	# 			products = place_du_marche.extract_product_list(url)
	# 			save_products(products)
	# 		else:
	# 			for key_last_level in sub_category_level_2:
	# 				print "Extracting for category "+key_last_level
	# 				products = place_du_marche.extract_product_list(sub_category_level_2[key_last_level]["url"])
	# 				save_products(products)

# get_place_du_marche_categories.delay()