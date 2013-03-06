#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from matcher.simserver.simserver import SessionServer

class IndexController(object):
	"""
		Index controller, this method can:
			- build complete index from database
			- perform a query against index
	"""

	BASE_PATH = '/tmp/dalliz/matcher'
	METHOD = 'tfidf' 

	def __init__(self, osm, ProductModel):
		"""
			Input :
				- osm : 'ooshop', 'monoprix' ...
				- ProductModel : database entity model for product exemple : MonoprixProduct
		"""
		self.osm = osm
		self.ProductModel = ProductModel
		self.dir_path = IndexController.BASE_PATH + '/' +self.osm
		self.service = SessionServer(self.dir_path)

	def build_all_index(self):
		"""
			Building the index from scratch.

		"""
		reg = re.compile(r'\b[a-zA-Z]{3,}\b')
		products = self.ProductModel.objects.filter(stemmed_text__isnull=False)
		documents = [{'id': p.id, 'tokens': reg.findall(p.stemmed_text)} for p in products]
		self.service.train(documents, method=IndexController.METHOD)
		self.service.index(documents)

	def query(self, document ):
		"""
			Querying index with a document
			Input :
				-document : {'tokens': [list of words]}
		"""
		return self.service.find_similar(document)

	def get_products(self, datetime = None):
		"""
			This method returns products as documents filtered by updated time lesser thant the 
			provided datetime.
		"""
		reg = re.compile(r'\b[a-zA-Z]{3,}\b')
		products = self.ProductModel.objects.filter(stemmed_text__isnull=False)
		if datetime is not None:
			products = products.filter(created__gte=datetime)
		return [{'id': p.id, 'tokens': reg.findall(p.stemmed_text)} for p in products]

	def add_products(self, products):
		"""
			Adding products to the index, if product id already exists in index, it will override it

			Input :
				- products = [{'id':,'tokens':..}]
		"""
		self.service.index(products)
		
