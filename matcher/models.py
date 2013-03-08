#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from django.db import models
from ooshop.models import NewProduct as OoshopProduct
from monoprix.models import NewProduct as MonoprixProduct
from auchan.models import Product as AuchanProduct

# Stems
class Stem(models.Model):
	word = models.TextField(null=True, unique = True)

	def __unicode__(self):
		return self.word

class BaseWord(models.Model):
	text = models.TextField(null=True, unique = True)
	stem = models.ForeignKey(Stem)

	def __unicode__(self):
		return '%s -> %s'%(self.text, self.stem)

# Matcher results
class Similarity(models.Model):
	query_osm = models.TextField()
	index_osm = models.TextField()

	monoprix_product = models.ForeignKey(MonoprixProduct, null = True)
	ooshop_product = models.ForeignKey(OoshopProduct, null = True)
	auchan_product = models.ForeignKey(AuchanProduct, null = True)

	score = models.FloatField()

	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		query_from = -1
		index_to = -1
		if query_osm == 'ooshop':
			query_from = ooshop_product
		if query_osm == 'monoprix':
			query_from = monoprix_product
		if query_osm == 'auchan':
			query_from = auchan_product

		if index_osm == 'ooshop':
			index_to = ooshop_product
		if index_osm == 'monoprix':
			index_to = monoprix_product
		if index_osm == 'auchan':
			index_to = auchan_product

		return 'From %s to %s, %s -> %s with score %f'%(query_osm, index_osm, query_from, index_to)

class PossibleMatch(models.Model):
	# TO DO : add user id
	monoprix_product = models.ForeignKey(MonoprixProduct, null = True)
	ooshop_product = models.ForeignKey(OoshopProduct, null = True)
	auchan_product = models.ForeignKey(AuchanProduct, null = True)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s | %s | %s'%(str(monoprix_product), str(ooshop_product), str(auchan_product))

class Match(models.Model):
	monoprix_product = models.ForeignKey(MonoprixProduct, null = True, unique = True)
	ooshop_product = models.ForeignKey(OoshopProduct, null = True, unique = True)
	auchan_product = models.ForeignKey(AuchanProduct, null = True, unique = True)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s | %s | %s'%(str(monoprix_product), str(ooshop_product), str(auchan_product))

class MatcherLog(models.Model):
	osm = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return 'Last update for %s : %s'%(osm, updated)
