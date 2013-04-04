#!/usr/bin/python
# -*- coding: utf-8 -*-

from cart.base.basecartcontroller import BaseCartController

from ooshop.models import Cart

class OoshopCartController(BaseCartController):
	"""
	"""
	def __init__(self, cart = None):
		super(OoshopCartController, self).__init__(Cart, cart)