#!/usr/bin/python
# -*- coding: utf-8 -*-

from cart.auchan.auchancartcontroller import AuchanCartController
from cart.monoprix.monoprixcartcontroller import MonoprixCartController
from cart.ooshop.ooshopcartcontroller import OoshopCartController

#--------------------------------------------------------------------------------------------------------------------------------------------
#
#													CUSTOM EXCEPTION
#
#--------------------------------------------------------------------------------------------------------------------------------------------

class ErrorNoOSMSet(Exception):
	"""
		Custom error : no osm set
	"""
	def __init__(self, osm):
		self.osm = osm
	def __str__(self):
		return repr(self.osm)

class ErrorNotProperOSM(Exception):
	"""
		Custom error : provided osm is not valid
	"""
	def __init__(self, osm):
		self.osm = osm
	def __str__(self):
		return repr(self.osm)


#--------------------------------------------------------------------------------------------------------------------------------------------
#
#													CARTS CONTROLLER CLASS
#
#--------------------------------------------------------------------------------------------------------------------------------------------

class DallizCartController(object):
	"""
		This class is responsible for 
	"""
	AVAILABLE_OSMS = {
		'ooshop': {
			'class': OoshopCartController
		},
		'monoprix': {
			'class': MonoprixCartController
		},
		'auchan': {
			'class': AuchanCartController
		}
	}

	def __init__(self, osm = 'monoprix', cart = None):
		if osm is None:
			raise ErrorNoOSMSet(osm)
		elif osm in DallizCartController.AVAILABLE_OSMS.keys():
			self.osm = osm
		else:
			raise ErrorNoOSMSet(osm)

		#self.carts = { osm:DallizCartController.AVAILABLE_OSMS[osm]['class']() for osm in DallizCartController.AVAILABLE_OSMS.keys()}
		self.carts = { osm:None for osm in DallizCartController.AVAILABLE_OSMS.keys()}
		if cart is not None:
			self.set_cart(cart, osm)

	def osm(function):
		"""
			This class ensures that a proper osm is set.
		"""
		def wrapper( self , *args, **kwargs) :
			if self.osm is None:
				ErrorNoOSMSet(self.osm)
			elif self.osm in DallizCartController.AVAILABLE_OSMS.keys():
				result = function( self , *args, **kwargs)
				return result
			else:
				raise ErrorNotProperOSM(self.osm)
		return wrapper

	def osm_verification(self, osm):
		"""
			Checks if osm is in valid
		"""
		return osm in DallizCartController.AVAILABLE_OSMS.keys()

	def set_osm(self, new_osm):
		if self.osm_verification(new_osm):
			self.osm = new_osm
		else:
			raise ErrorNotProperOSM(new_osm)

	def set_cart(self, cart, osm):
		"""
			Setting a cart to osm
		"""
		# First step : setting osm
		self.set_osm(osm)
		self.carts[osm] = cart

		# We now have to build other carts
		for other_osm in DallizCartController.AVAILABLE_OSMS.keys():
			if other_osm != osm:
				if self.carts[other_osm] is None:
					self.carts[other_osm] = DallizCartController.AVAILABLE_OSMS[other_osm]['class']()
				
				self.carts[other_osm].set_equivalent_cart(self.carts[osm].cart)

	@osm
	def add_product(self, product, quantity = 1):
		if self.carts[self.osm] is None:
			self.carts[self.osm] = DallizCartController.AVAILABLE_OSMS[self.osm]['class']()
		self.carts[self.osm].add_product(product, quantity)
		self.set_cart(self.carts[self.osm], self.osm)

	@osm
	def remove_product(self, product, quantity = None):
		if self.carts[self.osm] is None:
			self.carts[self.osm] = DallizCartController.AVAILABLE_OSMS[self.osm]['class']()
		self.carts[self.osm].remove_product(product, quantity)
		self.set_cart(self.carts[self.osm], self.osm)


	def empty(self):
		for osm, cart in self.carts.iteritems():
			if cart:
				cart.empty()



