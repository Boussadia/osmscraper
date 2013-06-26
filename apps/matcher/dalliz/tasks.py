#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from celery import Celery
from celery.task import periodic_task, task

from apps.matcher.dalliz.stemmer import DallizStemmer

celery = Celery('tasks', broker=settings.BROKER_URL)

@celery.task
def run_stemmer():
	DallizStemmer.run()