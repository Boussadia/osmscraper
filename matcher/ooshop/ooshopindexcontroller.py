#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import # Import because of modules names

from matcher.base.indexcontroller import IndexController

from ooshop.models import NewProduct as Product

class OoshopIndexController(IndexController):
	"""

	"""
	def __init__(self):
		super(OoshopIndexController, self).__init__(osm = 'ooshop', ProductModel = Product)
