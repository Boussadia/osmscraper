#!/usr/bin/python
# -*- coding: utf-8 -*-

from celery.task.schedules import crontab
from celery.task import periodic_task, task

from django.conf import settings
from celery import Celery

from scrapers.monoprix import Monoprix
from scrapers.telemarket import Telemarket
from scrapers.place_du_marche import Place_du_marche
from scrapers.coursengo import Coursengo

import monoprix
import place_du_marche
import telemarket
import coursengo

celery = Celery('tasks', broker=settings.BROKER_URL)

@periodic_task(run_every=crontab(minute=0, hour=22))
def perform_scraping():
	print "Begining scraping."
	
	try:
		print "Step 1 : Telemarket"
		telemarket.tasks.perform_scraping()
	except Exception as e :
		print e
		print "Aborting after error while executing telemarket scraper"
	else:
		print "Telemarket scraper executed properly"
		
	
	try:
		print "Step 2 : Monoprix"
		monoprix.tasks.perform_scraping()
	except Exception as e :
		print e
		print "Aborting after error while executing monoprix scraper"
	else:
		print "Monoprix scraper executed properly"
		

	try:
		print "Step 3 : Place du Marche"
		# place_du_marche.tasks.perform_scraping()
	except Exception as e :
		print e
		print "Aborting after error while executing place du marche scraper"
	else:
		print "Place du Marche scraper executed properly"
		

	try:
		print "Step 4 : Coursengo"
		# coursengo.tasks.perform_scraping()		
	except Exception as e :
		print e
		print "Aborting after error while executing coursengo scraper"
	else:
		print "Coursengo scraper executed properly"

@task
def migrate_monoprix_db():
	import re
	from osmscraper.utility import dictfetchall
	from django.db import connection
	REGEXP = re.compile(r'\W+')

	sql_query = (" SELECT id, unaccent(lower(title)) as title FROM monoprix_product ")

	cursor = connection.cursor()
	cursor.execute(sql_query)
	products = dictfetchall(cursor)
	for i in xrange(0,len(products)):
		dalliz_url = '-'.join(REGEXP.split(products[i]['title']))
		product = monoprix.models.Product.objects.get(id=products[i]['id'])
		product.dalliz_url = dalliz_url
		product.save()

@task
def migrate_categories():
	import re
	from osmscraper.utility import dictfetchall
	from django.db import connection
	from dalliz.models import Category_sub
	REGEXP = re.compile(r'\W+')

	sql_query = (" SELECT id, unaccent(lower(name)) as name FROM dalliz_category_sub ")

	cursor = connection.cursor()
	cursor.execute(sql_query)
	categories = dictfetchall(cursor)
	for i in xrange(0,len(categories)):
		url = '-'.join(REGEXP.split(categories[i]['name']))
		category = Category_sub.objects.get(id=categories[i]['id'])
		category.url = url
		category.save()


