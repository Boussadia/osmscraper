#!/usr/bin/python
# -*- coding: utf-8 -*-

from cart.base.basecartcontroller import BaseCartController

from monoprix.models import Cart

class MonoprixCartController(BaseCartController):
	"""
	"""
	def __init__(self, cart = None):
		super(MonoprixCartController, self).__init__(Cart, cart)