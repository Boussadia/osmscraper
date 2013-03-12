#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from django.db import models
from ooshop.models import NewProduct as OoshopProduct
from monoprix.models import NewProduct as MonoprixProduct
from auchan.models import Product as AuchanProduct
from ooshop.models import NewBrand as OoshopBrand
from monoprix.models import NewBrand as MonoprixBrand
from auchan.models import Brand as AuchanBrand
from dalliz.models import NewBrand as DallizBrand

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
class ProductSimilarity(models.Model):
	query_name = models.TextField()
	index_name = models.TextField()

	monoprix_product = models.ForeignKey(MonoprixProduct, null = True)
	ooshop_product = models.ForeignKey(OoshopProduct, null = True)
	auchan_product = models.ForeignKey(AuchanProduct, null = True)

	score = models.FloatField()

	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		query_from = -1
		index_to = -1
		if query_name == 'ooshop':
			query_from = ooshop_product
		if query_name == 'monoprix':
			query_from = monoprix_product
		if query_name == 'auchan':
			query_from = auchan_product

		if index_name == 'ooshop':
			index_to = ooshop_product
		if index_name == 'monoprix':
			index_to = monoprix_product
		if index_name == 'auchan':
			index_to = auchan_product

		return 'From %s to %s, %s -> %s with score %f'%(query_name, index_name, query_from, index_to)

class BrandSimilarity(models.Model):
	query_name = models.TextField()
	index_name = models.TextField()

	monoprix_brand = models.ForeignKey(MonoprixBrand, null = True)
	ooshop_brand = models.ForeignKey(OoshopBrand, null = True)
	auchan_brand = models.ForeignKey(AuchanBrand, null = True)
	dalliz_brand = models.ForeignKey(DallizBrand, null = True)

	score = models.FloatField()

	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		query_from = -1
		index_to = -1
		if query_name == 'ooshop':
			query_from = ooshop_brand
		if query_name == 'monoprix':
			query_from = monoprix_brand
		if query_name == 'auchan':
			query_from = auchan_brand

		if index_name == 'ooshop':
			index_to = ooshop_brand
		if index_name == 'monoprix':
			index_to = monoprix_brand
		if index_name == 'auchan':
			index_to = auchan_brand

		return 'From %s to %s, %s -> %s with score %f'%(query_name, index_name, query_from, index_to)

class PossibleMatch(models.Model):
	# TO DO : add user id
	monoprix_product = models.ForeignKey(MonoprixProduct, null = True)
	ooshop_product = models.ForeignKey(OoshopProduct, null = True)
	auchan_product = models.ForeignKey(AuchanProduct, null = True)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s | %s | %s'%(str(monoprix_product), str(ooshop_product), str(auchan_product))

class ProductMatch(models.Model):
	monoprix_product = models.ForeignKey(MonoprixProduct, null = True, unique = True)
	ooshop_product = models.ForeignKey(OoshopProduct, null = True, unique = True)
	auchan_product = models.ForeignKey(AuchanProduct, null = True, unique = True)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s | %s | %s'%(str(monoprix_product), str(ooshop_product), str(auchan_product))

class BrandMatch(models.Model):
	monoprix_brand = models.ForeignKey(MonoprixBrand, null = True)
	ooshop_brand = models.ForeignKey(OoshopBrand, null = True)
	auchan_brand = models.ForeignKey(AuchanBrand, null = True)
	dalliz_brand = models.ForeignKey(DallizBrand, null = True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = (("dalliz_brand", "auchan_brand"),("dalliz_brand", "ooshop_brand"),("dalliz_brand", "monoprix_brand"),)

	def __unicode__(self):
		return '%s | %s | %s'%(str(monoprix_brand), str(ooshop_brand), str(auchan_brand))

class MatcherLog(models.Model):
	name = models.TextField()
	type = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return 'Last update for %s : %s'%(name, updated)
