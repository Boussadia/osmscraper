#!/usr/bin/python
# -*- coding: utf-8 -*-

from cart.auchan.auchancartcontroller import AuchanCartController
from cart.monoprix.monoprixcartcontroller import MonoprixCartController
from cart.ooshop.ooshopcartcontroller import OoshopCartController

from cart.models import MetaCart

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

	def __init__(self, osm = 'monoprix', metacart = None):
		if osm is None:
			raise ErrorNoOSMSet(osm)
		elif osm in DallizCartController.AVAILABLE_OSMS.keys():
			self.osm = osm
		else:
			raise ErrorNoOSMSet(osm)

		if metacart is not None:
			self.metacart = metacart
		else:
			self.metacart = MetaCart(current_osm = self.osm)
			self.metacart.save()

		self.carts = {}
		for osm, value in DallizCartController.AVAILABLE_OSMS.iteritems():
			current_cart = getattr(self.metacart, osm+'_cart')
			cart_controller = value['class'](cart = current_cart)
			self.carts[osm] =  cart_controller
			if current_cart is None:
				setattr(self.metacart, osm+'_cart', cart_controller.cart)
				self.metacart.save()

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
			self.metacart.current_osm = new_osm
			self.metacart.save()
		else:
			raise ErrorNotProperOSM(new_osm)

	def set_cart(self, cart, osm):
		"""
			Setting a cart to osm
		"""
		# First step : setting osm
		self.set_osm(osm)
		self.carts[osm] = cart
		equivalences = {}
		setattr(self.metacart, osm+'_cart', cart.cart)

		# We now have to build other carts
		for other_osm in DallizCartController.AVAILABLE_OSMS.keys():
			if other_osm != osm:
				if self.carts[other_osm] is None:
					self.carts[other_osm] = DallizCartController.AVAILABLE_OSMS[other_osm]['class']()
					try:
						setattr(self.metacart, other_osm+'_cart', self.carts[other_osm].cart)
					except Exception, e:
						pass
				equivalences[other_osm] = self.carts[other_osm].set_equivalent_cart(self.carts[osm].cart)

		self.metacart.save()

		# Setting equivalent content for ohter osms
		for other_osm in DallizCartController.AVAILABLE_OSMS.keys():
			if other_osm != osm:
				for other_osm_bis in DallizCartController.AVAILABLE_OSMS.keys():
					if other_osm_bis != osm and other_osm_bis != other_osm:
						for content in  equivalences[other_osm].keys():
							try:
								other_content = equivalences[other_osm][content]['content']
							except Exception, e:
								pass

							try:
								other_content_bis = equivalences[other_osm_bis][content]['content']
							except Exception, e:
								pass
							
							try:
								setattr(other_content_bis, other_content.cart.osm+'_content', other_content)
							except Exception, e:
								pass
							
							try:
								setattr(content, other_content_bis.cart.osm+'_content', other_content_bis)
							except Exception, e:
								pass
							
							try:
								setattr(content, other_content.cart.osm+'_content', other_content)
							except Exception, e:
								pass

							try:
								other_content_bis.save()
							except Exception, e:
								pass





	@osm
	def add_product(self, product, quantity = 1):
		if self.carts[self.osm] is None:
			self.carts[self.osm] = DallizCartController.AVAILABLE_OSMS[self.osm]['class']()
		self.carts[self.osm].add_product(product, quantity, is_user_added = True, is_match = False, is_suggested = False, is_user_set = False)
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



