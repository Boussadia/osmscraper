#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import # Import because of modules names

from matcher.base.indexcontroller import IndexController

from monoprix.models import NewProduct as Product

class MonoprixIndexController(IndexController):
	"""

	"""
	def __init__(self):
		super(MonoprixIndexController, self).__init__(osm = 'monoprix', ProductModel = Product)
