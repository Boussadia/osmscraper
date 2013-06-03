#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

from django.conf import settings
from django.core.mail import send_mail

from celery import Celery
from celery.task import periodic_task, task

from apps.scrapers.monoprix.monoprixscraper import MonoprixScraper

celery = Celery('tasks', broker=settings.BROKER_URL)

@celery.task
def get_categories():
	"""
		This task is reponsible for retrieving all categories.
	"""
	scraper = MonoprixScraper()
	scraper.get_all_categories()

	# VERY IMPORTANT, ALWAYS CALL THIS TASK IN ORDER TO HAVE AN INFINITE LOOP
	what_to_do_next.delay()

@celery.task
def get_products_category(categories):
	"""
		This task is reponsible for retrieving products of a category and location.

		Input :
			- categories = [{
				'url':...,
				'location':...
			}]
	"""
	scraper = MonoprixScraper()

	for category in categories:
		scraper.get_list_products_for_category(category_url = category['url'], location = category['location'], save = True)
		# time.sleep(1) # Temporisation in order not to flood server


	# VERY IMPORTANT, ALWAYS CALL THIS TASK IN ORDER TO HAVE AN INFINITE LOOP
	what_to_do_next.delay()

@celery.task
def get_products(products):
	"""
		This task is reponsible for retrieving products of a product and location.

		Input :
			- products = [{
				'url':...,
				'location':...
			}]
	"""
	scraper = MonoprixScraper()

	for product in products:
		try:
			url = product['url']
			location = {}
			if 'location' in product:
				location = product['location']
			scraper.get_product_info(product_url = url, location = location, save = True)
			# time.sleep(1) # Temporisation in order not to flood server
		except Exception, e:
			print 'Error in get_products tasks :'
			print product
			print e


	# VERY IMPORTANT, ALWAYS CALL THIS TASK IN ORDER TO HAVE AN INFINITE LOOP
	what_to_do_next.delay()



@celery.task
def what_to_do_next():
	scraper = MonoprixScraper()
	rule = scraper.what_to_do_next()

	if rule['type'] == 'categories':
		get_categories.delay()
	elif rule['type'] == 'category_products':
		categories = rule['categories']
		get_products_category.delay(categories = categories)
	elif rule['type'] == 'products':
		products = rule['products']
		get_products.delay(products = products)
	elif rule['type'] == 'global':
		delay = rule['delay']
		what_to_do_next.apply_async(countdown=delay)

@celery.task
def simple_update():
	from monoprix.models import Product as Product, Promotion
	from datetime import datetime, timedelta
	scraper = MonoprixScraper()
	# First get uncomplete products
	products = Product.objects.filter(exists = True, stemmed_text__isnull = True)

	if len(products) >0:
		scraper.get_product_info(products[0].url, save=True)
		simple_update.apply_async(countdown = 2)
	else:
		products = Product.objects.filter(exists = True, updated__lte=datetime.now()-timedelta(hours = 24))
		if len(products)>0:
			scraper.get_product_info(products[0].url, save=True)
			simple_update.apply_async(countdown = 2)
		else:
			# Now getting multi promotions pages
			promotions = Promotion.objects.filter(availability = True, type = Promotion.MULTI, content__id__isnull = True)
			if len(promotions)>0:
				scraper.get_product_info(promotions[0].url, save=True)
				simple_update.apply_async(countdown = 2)
			else:
				simple_update.apply_async(countdown = 3600)

