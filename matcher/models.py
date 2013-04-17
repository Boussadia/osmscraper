#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from django.db import models
from ooshop.models import Product as OoshopProduct
from monoprix.models import Product as MonoprixProduct
from auchan.models import Product as AuchanProduct
from ooshop.models import Brand as OoshopBrand
from monoprix.models import Brand as MonoprixBrand
from auchan.models import Brand as AuchanBrand
from dalliz.models import Brand as DallizBrand

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
		if self.query_name == 'ooshop':
			query_from = self.ooshop_product
		if self.query_name == 'monoprix':
			query_from = self.monoprix_product
		if self.query_name == 'auchan':
			query_from = self.auchan_product

		if self.index_name == 'ooshop':
			index_to = self.ooshop_product
		if self.index_name == 'monoprix':
			index_to = self.monoprix_product
		if self.index_name == 'auchan':
			index_to = self.auchan_product

		return '%s : From %s to %s, %s -> %s with score %f'%(self.created, self.query_name, self.index_name, query_from, index_to, self.score)

class NoProductSimilarity(models.Model):
	monoprix_product = models.ForeignKey(MonoprixProduct, null = True)
	ooshop_product = models.ForeignKey(OoshopProduct, null = True)
	auchan_product = models.ForeignKey(AuchanProduct, null = True)

	class Meta:
		unique_together = (("monoprix_product", "ooshop_product"),("monoprix_product", "auchan_product"),("ooshop_product", "auchan_product"),)

	def __unicode__(self):
		if self.monoprix_product is not None:
			product_1 = self.monoprix_product
		elif self.auchan_product is not None:
			product_1 = self.auchan_product
		elif self.ooshop_product is not None:
			product_1 = self.ooshop_product

		if self.ooshop_product is not None:
			product_2 = self.ooshop_product
		elif self.auchan_product is not None:
			product_2 = self.auchan_product
		elif self.monoprix_product is not None:
			product_2 = self.monoprix_product

		return 'No match : %s <-/-> %s'%(product_1, product_2)

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
		if self.query_name == 'ooshop':
			query_from = self.ooshop_brand
		if self.query_name == 'monoprix':
			query_from = self.monoprix_brand
		if self.query_name == 'auchan':
			query_from = self.auchan_brand
		if self.query_name == 'dalliz':
			query_from = self.dalliz_brand

		if self.index_name == 'ooshop':
			index_to = self.ooshop_brand
		if self.index_name == 'monoprix':
			index_to = self.monoprix_brand
		if self.index_name == 'auchan':
			index_to = self.auchan_brand
		if self.index_name == 'dalliz':
			index_to = self.dalliz_brand

		return '%s : From %s to %s, %s -> %s with score %f'%(self.created, self.query_name, self.index_name, query_from, index_to, self.score)

class ProductMatch(models.Model):
	monoprix_product = models.ForeignKey(MonoprixProduct, null = True, unique = True)
	ooshop_product = models.ForeignKey(OoshopProduct, null = True, unique = True)
	auchan_product = models.ForeignKey(AuchanProduct, null = True, unique = True)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s | %s | %s'%(str(self.monoprix_product), str(self.ooshop_product), str(self.auchan_product))

class BrandMatch(models.Model):
	monoprix_brand = models.ForeignKey(MonoprixBrand, null = True)
	ooshop_brand = models.ForeignKey(OoshopBrand, null = True)
	auchan_brand = models.ForeignKey(AuchanBrand, null = True)
	dalliz_brand = models.ForeignKey(DallizBrand)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = (("dalliz_brand", "auchan_brand"),("dalliz_brand", "ooshop_brand"),("dalliz_brand", "monoprix_brand"),)

	def __unicode__(self):
		return '%s | %s | %s'%(str(self.monoprix_brand), str(self.ooshop_brand), str(self.auchan_brand))

class MatcherLog(models.Model):
	name = models.TextField()
	type = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return 'Last update for %s : %s'%(self.name, self.updated)
