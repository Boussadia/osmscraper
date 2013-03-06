#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

import datetime

from matcher.ooshop.ooshopindexcontroller import OoshopIndexController
from matcher.monoprix.monoprixindexcontroller import MonoprixIndexController

from matcher.models import MatcherLog
from matcher.models import Similarity


class Matcher(object):
	"""
		This class is responsible for managing the different indexes of osms products.
		It detects when new products are added to the database, creates similarities between products
		and save matches in database.

	"""
	DEFAULT_INDEXER_CLASSES = [OoshopIndexController, MonoprixIndexController]
	def __init__(self, indexer_classes = DEFAULT_INDEXER_CLASSES):
		self.indexers = [ c() for c in indexer_classes]
		self.products = None

	def set_new_products(self):
		time_filter = None
		self.products = {}
		for indexer in self.indexers:
			osm = indexer.osm
			# Getting time of last matcher process for this osm
			logs = MatcherLog.objects.filter(osm = osm).order_by('-created')
			if len(logs)>0:
				time_filter = logs[0].created

			self.products[osm] = indexer.get_products(time_filter)

	def set_all_products(self):
		self.products = { indexer.osm:indexer.get_products() for indexer in self.indexers}

	def get_indexer_by_name(self, name):
		"""
			Return indexer matching name
		"""
		result_indexer = None
		for indexer in self.indexers:
			if name == indexer.osm:
				result_indexer = indexer
				break
		return result_indexer

	def run(self, override = False):
		"""
			This method will go through every indexer, get new products and perform query.
			It will then save the similarities into the database.
		"""

		if not override:
			# Update with new products
			self.set_new_products()

			# Update all indexes
			for osm, products in self.products.iteritems():
				if len(products) >0:
					# New products detected, building new index for corresponding indexer
					indexer = self.get_indexer_by_name(osm)
					indexer.add_products(products)
		else:
			# Set all products
			self.set_all_products()
			# Rebuild all indexes
			[indexer.build_all_index() for indexer in self.indexers]

		
		# Performing queries
		for osm_query, products in self.products.iteritems():
			for indexer in self.indexers:
				if osm_query == indexer.osm:
					# Do not perform query if products in osm
					continue
				# Performing query
				similarities = [ {'id':product['id'], 'indexer_osm':indexer.osm, 'query_osm':osm_query, 'sims': indexer.query(product)} for product in products]
				self.save_similarities(similarities)
				self.save_log(osm_query)

	def save_similarities(self, similarities):
		"""
			Saving similarities to database

			Input : 
				- similarities = [{'id':, 'indexer_osm':, 'query_osm':, 'sims': [(id, score, ??)]}]
		"""
		similarities_db_list = []
		for s in similarities:
			ooshop_product_id = None
			monoprix_product_id = None
			auchan_product_id = None

			if s['query_osm'] == 'ooshop':
				ooshop_product_id = s['id']
			if s['query_osm'] == 'monoprix':
				monoprix_product_id = s['id']
			if s['query_osm'] == 'auchan':
				auchan_product_id = s['id']

			for id_doc, score, last_arg in s['sims']:
				if s['indexer_osm'] == 'ooshop':
					ooshop_product_id = id_doc
				if s['indexer_osm'] == 'monoprix':
					monoprix_product_id = id_doc
				if s['indexer_osm'] == 'auchan':
					auchan_product_id = id_doc

				sim_db = Similarity(
					query_osm = s['query_osm'],
					index_osm = s['indexer_osm'],
					monoprix_product_id = monoprix_product_id,
					ooshop_product_id = ooshop_product_id,
					auchan_product_id = auchan_product_id,
					score = score
				)
				similarities_db_list.append(sim_db)

		# Creating data in bulk
		Similarity.objects.bulk_create(similarities_db_list)

	def save_log(self, osm):
		"""
			Saving log for osm
		"""
		MatcherLog(osm = osm).save()



