#!/usr/bin/python
# -*- coding: utf-8 -*-

from cart.base.basecartcontroller import BaseCartController

from auchan.models import Cart

class AuchanCartController(BaseCartController):
	"""
	"""
	def __init__(self, cart = None):
		super(AuchanCartController, self).__init__(Cart, cart)
