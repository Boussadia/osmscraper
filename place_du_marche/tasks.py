#!/usr/bin/python
# -*- coding: utf-8 -*-

from celery.task.schedules import crontab
from celery.task import periodic_task

from django.conf import settings
from celery import Celery

from scrapers.place_du_marche import Place_du_marche

celery = Celery('tasks', broker=settings.BROKER_URL)
place_du_marche = Place_du_marche()

@periodic_task(run_every=crontab(minute="*/1"))
def get_place_du_marche_categories():
	place_du_marche.get_menu()


# get_place_du_marche_categories.delay()