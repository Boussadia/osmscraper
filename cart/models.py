#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from django.db import models
from django.contrib.sessions.models import Session

from auchan.models import Cart as AuchanCart
from monoprix.models import Cart as MonoprixCart
from ooshop.models import Cart as OoshopCart

# Cart association handling
class MetaCart(models.Model):
	monoprix_cart = models.ForeignKey(MonoprixCart, null = True)
	auchan_cart = models.ForeignKey(AuchanCart, null = True)
	ooshop_cart = models.ForeignKey(OoshopCart, null = True)
	current_osm = models.CharField(max_length = 100, default = 'monoprix')
	session = models.ForeignKey(Session, null = True)

	def __unicode__(self):
		return 'Current OSM : %s. Monoprix : %s, Auchan: %s, Ooshop : %s'%(self.current_osm, self.monoprix_cart, self.auchan_cart, self.ooshop_cart)
