#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import # Import because of modules names

from django.conf import settings
from celery import Celery
from celery.task import periodic_task, task

from apps.matcher.auchan.auchanstemmer import AuchanStemmer
from apps.matcher.monoprix.monoprixstemmer import MonoprixStemmer
from apps.matcher.ooshop.ooshopstemmer import OoshopStemmer

from ooshop.models import Product as OoshopProduct
from monoprix.models import Product as MonoprixProduct
from auchan.models import Product as AuchanProduct

class DallizStemmer(object):
	"""
		This class is rsponsible for stemming products.
	"""

	OSMS = ['auchan', 'ooshop', 'monoprix']

	@staticmethod
	def run():
		"""
			Running process.
		"""

		osms = DallizStemmer.OSMS

		for osm in osms:
			print 'Working on %s'%osm.capitalize()
			product_class_name = '%sProduct'%(osm.capitalize())
			stemmer_class_name = '%sStemmer'%(osm.capitalize())

			OSMProduct = globals()[product_class_name]
			Stemmer = globals()[stemmer_class_name]

			products = OSMProduct.objects.filter(html__isnull = False)
			count = products.count()
			i = 0

			for product in products:
				i = i+1
				progress = 100
				if count>0:
					progress = round(i*10000/count)/100.0
				print 'Stemming %s (Progress : %f %s)'%(product.name, progress, '%')
				product.stemmed_text = Stemmer(product.html).stem_text()
				product.save()

celery = Celery('tasks', broker=settings.BROKER_URL)

@celery.task
def run_stemmer():
	DallizStemmer.run()
