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

class PossibleMatch(models.Model):
	# TO DO : add user id
	monoprix_product = models.ForeignKey(MonoprixProduct, null = True)
	ooshop_product = models.ForeignKey(OoshopProduct, null = True)
	auchan_product = models.ForeignKey(AuchanProduct, null = True)

class Match(models.Model):
	# TO DO : add user id
	monoprix_product = models.ForeignKey(MonoprixProduct, null = True)
	ooshop_product = models.ForeignKey(OoshopProduct, null = True)
	auchan_product = models.ForeignKey(AuchanProduct, null = True)
