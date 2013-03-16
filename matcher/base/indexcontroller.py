#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from matcher.simserver.simserver import SessionServer
from osmscraper.unaccent import unaccent 

class IndexController(object):
	"""
		Index controller, this method can:
			- build complete index from database
			- perform a query against index
	"""

	BASE_PATH = '/tmp/dalliz/matcher'
	METHOD = 'tfidf' 

	def __init__(self, name, type, Model):
		"""
			Input :
				- name : 'ooshop', 'monoprix' ...
				- Model : database entity model for exemple : MonoprixProduct
		"""
		self.name = name
		self.type = type
		self.Model = Model
		self.dir_path = IndexController.BASE_PATH + '/' +self.type+'/'+self.name
		self.service = SessionServer(self.dir_path)

	def build_all_index(self):
		"""
			Building the index from scratch.

		"""
		reg = re.compile(r'\b[a-zA-Z]{3,}\b')
		documents = self.Model.objects.all()
		documents = [{'id': d.id, 'tokens': reg.findall(unaccent(d.name.lower()))} for d in documents]
		self.service.train(documents, method=IndexController.METHOD)
		self.service.index(documents)

	def query(self, document ):
		"""
			Querying index with a document
			Input :
				-document : {'tokens': [list of words]}
		"""
		return self.service.find_similar(document)

	def get_documents(self, datetime = None):
		"""
			This method returns documents filtered by updated time lesser thant the 
			provided datetime.
		"""
		reg = re.compile(r'\b[a-zA-Z]{3,}\b')
		documents = self.Model.objects.all()
		if datetime is not None:
			documents = documents.filter(created__gte=datetime)
		return [{'id': d.id, 'tokens': reg.findall(unaccent(d.name.lower()))} for d in documents]

	def add_documents(self, documents):
		"""
			Adding documents to the index, if document id already exists in index, it will override it

			Input :
				- documents = [{'id':,'tokens':..}]
		"""
		try:
			self.service.index(documents)
		except AttributeError, e:
			self.service.train(documents, method=IndexController.METHOD)

class BrandIndexController(IndexController):
	"""
		Index controller, this method can:
			- build complete index from database
			- perform a query against index
	"""

	BASE_PATH = '/tmp/dalliz/matcher/brand'

	def __init__(self, osm, BrandModel):
		"""
			Input :
				- osm : 'ooshop', 'monoprix' ...
				- ProductModel : database entity model for exemple : MonoprixProduct
		"""
		super(BrandIndexController, self).__init__(osm, 'brand', BrandModel)

class ProductIndexController(IndexController):
	"""
		Index controller, this method can:
			- build complete index from database
			- perform a query against index
	"""

	BASE_PATH = '/tmp/dalliz/matcher/products'

	def __init__(self, osm, ProductModel):
		"""
			Input :
				- osm : 'ooshop', 'monoprix' ...
				- ProductModel : database entity model for exemple : MonoprixProduct
		"""
		super(ProductIndexController, self).__init__(osm, 'products', ProductModel)

	def build_all_index(self):
		"""
			Building the index from scratch.

		"""
		reg = re.compile(r'\b[a-zA-Z]{3,}\b')
		products = self.Model.objects.filter(stemmed_text__isnull=False)
		documents = [{'id': p.id, 'tokens': reg.findall(p.stemmed_text)} for p in products]
		if len(documents)>0:
			self.service.train(documents, method=IndexController.METHOD)
			self.service.index(documents)

	def get_documents(self, datetime = None):
		"""
			This method returns products as documents filtered by updated time lesser thant the 
			provided datetime.
		"""
		reg = re.compile(r'\b[a-zA-Z]{3,}\b')
		products = self.Model.objects.filter(stemmed_text__isnull=False)
		if datetime is not None:
			products = products.filter(created__gte=datetime)
		return [{'id': p.id, 'tokens': reg.findall(p.stemmed_text)} for p in products]
