#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import math

from django.db import connection, transaction

from telemarket.models import Monoprix_matching
from telemarket.models import Product as Telemarket_product


from engine import Engine
from engine import Product_engine

class OSM_matcher(object):
	"""docstring for OSM_matcher"""
	def __init__(self, sql_query, engine_class = Engine):
		super(OSM_matcher, self).__init__()
		self.__sql_query__ = sql_query
		self.__engine_class__ = engine_class
		self.__engine__ = None
		self.__matches__ = {}

	def set_matches(self, matches):
		self.__matches__ = matches

	def get_matches(self):
		return self.__matches__

	def get_sql_query(self):
		return self.__sql_query__

	def get_data_from_db(self):
		cursor = connection.cursor()
		cursor.execute(self.get_sql_query())
		return self.dictfetchall(cursor)

	def get_engine_class(self):
		return self.__engine_class__

	def get_engine(self):
		return self.__engine__

	def make_index(self):
		engine = self.get_engine_class()(list(self.get_data_from_db()))
		engine.tokenize()
		self.__engine__ = engine

	def dictfetchall(self, cursor):
		"Generator of all rows from a cursor"
		desc = cursor.description
		for row in cursor.fetchall():
			yield dict(zip([col[0] for col in desc], row))

	def start_process(self, other_products):
		# Indexation
		self.make_index()
		engine = self.get_engine()
		matches = {}
		for other_product in other_products:
			query = other_product["content"]
			engine.process_query(query)
			matches[other_product['id']] = engine.get_possible_matches(query)

		self.set_matches(matches)

	def show_results(self):
		all_matches = self.get_matches()

		for id_other_product, possible_matches in all_matches.iteritems():
			score_max = 0
			id_max = 1
			for i in xrange(0,len(possible_matches)):
				if possible_matches[i]['score']>score_max:
					score_max = possible_matches[i]['score']
					id_max = possible_matches[i]['id']

			print str(id_other_product)+' : '+str(id_max)+' -> '+str(score_max)


class Dalliz_matcher(OSM_matcher):
	def __init__(self): 
		super(Dalliz_matcher, self).__init__("SELECT id, unaccent(lower(name)) as content FROM dalliz_brand ORDER BY length(name) DESC")

	def brands(self):
		brands_from_db = self.get_data_from_db()
		for brand in brands_from_db:
			yield brand

	def save_brands_telemarket(self):
		all_matches = self.get_matches()

		for id_other_product, possible_matches in all_matches.iteritems():
			score_max = 0
			id_max = 1
			for i in xrange(0,len(possible_matches)):
				if possible_matches[i]['score']>score_max:
					score_max = possible_matches[i]['score']
					id_max = possible_matches[i]['id']

			print str(id_other_product)+' : '+str(id_max)+' -> '+str(score_max)






class Telemarket_matcher(OSM_matcher):
	def __init__(self): 
		super(Telemarket_matcher, self).__init__("SELECT telemarket_product.id, unaccent(lower(title)) as content, telemarket_unit_dalliz_unit.to_unit_id as unit, telemarket_product.category_id as category FROM telemarket_product JOIN telemarket_unit_dalliz_unit ON telemarket_product.unit_id = telemarket_unit_dalliz_unit.from_unit_id ORDER BY length(title)", Product_engine)

	def get_categories(self, sql_categories):
		cursor = connection.cursor()
		cursor.execute(sql_categories)
		return self.dictfetchall(cursor)

	def products(self):
		products_from_db = self.get_data_from_db()
		categories = list(self.get_categories("SELECT category_final_id as telemarket_category, category_sub_id as category FROM telemarket_category_final_dalliz_category"))
		for product in products_from_db:
			product['categories'] = []
			for j in xrange(0,len(categories)):
				if categories[j]['telemarket_category'] == product['category']:
					product['categories'].append(categories[j]['category'])
			yield product

	def make_index(self):
		engine = self.get_engine_class()(list(self.products()))
		engine.tokenize()
		self.__engine__ = engine




class Monoprix_matcher(OSM_matcher):
	def __init__(self): 
		super(Monoprix_matcher, self).__init__("SELECT monoprix_product.id, (unaccent(lower(monoprix_brand.name))||' '||unaccent(lower(title)) )as content, monoprix_unit_dalliz_unit.to_unit_id as unit, monoprix_product.category_id as category FROM monoprix_product JOIN monoprix_unit_dalliz_unit ON monoprix_product.unit_id = monoprix_unit_dalliz_unit.from_unit_id JOIN monoprix_brand ON monoprix_brand.id = monoprix_product.brand_id ORDER BY length(title) DESC", Product_engine)

	def get_categories(self, sql_categories):
		cursor = connection.cursor()
		cursor.execute(sql_categories)
		return self.dictfetchall(cursor)

	def make_index(self):
		engine = self.get_engine_class()(list(self.products()))
		engine.tokenize()
		self.__engine__ = engine

	def products(self):
		products_from_db = self.get_data_from_db()
		categories = list(self.get_categories("SELECT category_final_id as monoprix_category, category_sub_id as category FROM monoprix_category_final_dalliz_category"))
		for product in products_from_db:
			product['categories'] = []
			for j in xrange(0,len(categories)):
				if categories[j]['monoprix_category'] == product['category']:
					product['categories'].append(categories[j]['category'])
			yield product

	def start_process(self, other_products):
		# Indexation
		self.make_index()
		engine = self.get_engine()
		matches = {}
		for other_product in other_products:
			query = other_product["content"]
			engine.set_possible_products(other_product)
			matches[other_product['id']] = engine.get_possible_matches(query)
			self.save_matches_telemarket(other_product['id'], matches[other_product['id']]) 

		self.set_matches(matches)

	def save_matches_telemarket(self, id_telemarket_product,matches ):
		try:
			print 'Saving matcher result'
			for i in xrange(0,len(matches)):
				id_monoprix = matches[i]['id']
				score = matches[i]['score']
				relation, created = Monoprix_matching.objects.get_or_create(telemarket_product_id = id_telemarket_product, monoprix_product_id = id_monoprix, defaults={'score': score})
				relation.score = score
				relation.save()
		except Exception, e:
			print e 



