#!/usr/bin/python
# -*- coding: utf-8 -*-

from celery.task.schedules import crontab
from celery.task import periodic_task

from django.conf import settings
from celery import Celery

from scrapers.monoprix import Monoprix
from scrapers.telemarket import Telemarket
from scrapers.place_du_marche import Place_du_marche

import monoprix
import place_du_marche
import telemarket

celery = Celery('tasks', broker=settings.BROKER_URL)

@periodic_task(run_every=crontab(minute=0, hour=22))
def perform_scraping():
	telemarket.tasks.perform_scraping()
	monoprix.tasks.perform_scraping()
	place_du_marche.tasks.perform_scraping()

# perform_scraping.delay()