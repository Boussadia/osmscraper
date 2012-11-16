#!/usr/bin/python
# -*- coding: utf-8 -*-

from celery.task.schedules import crontab
from celery.task import periodic_task, task

from django.conf import settings
from celery import Celery

from osmscraper.telemarket_matching import *

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
		monoprix.tasks.perform_update_scraping()
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

	print "Performing matching"
	perform_monoprix_telemarket_matching()