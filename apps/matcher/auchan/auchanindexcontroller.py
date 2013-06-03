#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import # Import because of modules names

from apps.matcher.base.indexcontroller import ProductIndexController
from apps.matcher.base.indexcontroller import BrandIndexController

from auchan.models import Product
from auchan.models import Brand

class AuchanProductIndexController(ProductIndexController):
	"""

	"""
	def __init__(self):
		super(AuchanProductIndexController, self).__init__(osm = 'auchan', ProductModel = Product)

class AuchanBrandIndexController(BrandIndexController):
	"""

	"""
	def __init__(self):
		super(AuchanBrandIndexController, self).__init__(osm = 'auchan', BrandModel = Brand)
