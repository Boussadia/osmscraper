#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import # Import because of modules names

from matcher.base.indexcontroller import BrandIndexController

from dalliz.models import NewBrand as Brand

class DallizBrandIndexController(BrandIndexController):
	"""

	"""
	def __init__(self):
		super(DallizBrandIndexController, self).__init__(osm = 'dalliz', BrandModel = Brand)
