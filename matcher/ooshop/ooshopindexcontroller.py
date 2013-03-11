#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import # Import because of modules names

from matcher.base.indexcontroller import ProductIndexController
from matcher.base.indexcontroller import BrandIndexController

from ooshop.models import NewProduct as Product
from ooshop.models import NewBrand as Brand 

class OoshopProductIndexController(ProductIndexController):
	"""

	"""
	def __init__(self):
		super(OoshopProductIndexController, self).__init__(osm = 'ooshop', ProductModel = Product)

class OoshopBrandIndexController(BrandIndexController):
	"""

	"""
	def __init__(self):
		super(OoshopBrandIndexController, self).__init__(osm = 'ooshop', BrandModel = Brand)
