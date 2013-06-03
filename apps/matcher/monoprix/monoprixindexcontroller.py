#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import # Import because of modules names

from apps.matcher.base.indexcontroller import ProductIndexController
from apps.matcher.base.indexcontroller import BrandIndexController

from monoprix.models import Product
from monoprix.models import Brand

class MonoprixProductIndexController(ProductIndexController):
	"""

	"""
	def __init__(self):
		super(MonoprixProductIndexController, self).__init__(osm = 'monoprix', ProductModel = Product)

class MonoprixBrandIndexController(BrandIndexController):
	"""

	"""
	def __init__(self):
		super(MonoprixBrandIndexController, self).__init__(osm = 'monoprix', BrandModel = Brand)
