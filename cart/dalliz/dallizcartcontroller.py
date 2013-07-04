#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import connection

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
		"""
			This method adds a product that is not in the cart

			Input :
				- product : product database entity
				- quantity (int ) : amount of products to add
		"""
		if self.carts[self.osm] is None:
			self.carts[self.osm] = DallizCartController.AVAILABLE_OSMS[self.osm]['class']()
		cart_content = self.carts[self.osm].add_product(product, quantity, is_user_added = True, is_match = False, is_suggested = False, is_user_set = False)

		equivalent_contents = {}

		for osm in DallizCartController.AVAILABLE_OSMS.keys():
			if osm != self.osm:
				if self.carts[osm] is None:
					self.carts[osm] = DallizCartController.AVAILABLE_OSMS[self.osm]['class']()

				equivalent_contents[osm] = self.carts[osm].generate_equivalent_content(cart_content, self.osm)
		
		for osm in equivalent_contents.keys():
			if osm != self.osm:
				for other_osm in equivalent_contents.keys():
					if other_osm != osm and other_osm != self.osm:
						try:
							other_content = equivalent_contents[osm]['content']
						except Exception, e:
							pass

						try:
							other_content_bis = equivalent_contents[other_osm]['content']
						except Exception, e:
							pass
						
						try:
							setattr(other_content_bis, other_content.cart.osm+'_content', other_content)
						except Exception, e:
							pass
						
						try:
							setattr(other_content, other_content_bis.cart.osm+'_content', other_content_bis)
						except Exception, e:
							pass

						try:
							other_content_bis.save()
						except Exception, e:
							pass

						try:
							other_content.save()
						except Exception, e:
							pass

	@osm
	def add(self, cart_content, quantity = 1):
		"""
			This method increases quantity of a product that is already in the cart. It operates on a cart_content. If the product is not in the cart, use 
			@add_product method.

			Input :
				- cart_content : database entity foir a cart content
				- quantity (int) : how much products to add to cart
		"""

		# First set new quantity to cart content
		cart_content.quantity = cart_content.quantity + quantity
		controller = self.carts[self.osm]
		cart_content.save()

		new_quantity = cart_content.quantity
		base_product = cart_content.product

		# Setting up equivalent quantities for equivalent contents
		for osm in DallizCartController.AVAILABLE_OSMS.keys():
			if osm != self.osm:
				equivalent_content = getattr(cart_content, '%s_content'%(osm))

				if equivalent_content is not None:
					equivalent_product = equivalent_content.product

					# Computing equivalent content
					equivalent_quantity = controller.generate_equivalent_quantity(base_product, equivalent_product, new_quantity)

					# Setting equivalent quantity to equiuvalent content
					equivalent_content.quantity = equivalent_quantity
					equivalent_content.save()


	@osm
	def remove(self, cart_content, quantity = None):
		"""
			This method either completely removes a product from a cart or decreases its quantity. It works with 
			cart contents.

			Input : 
				- content : cart content entity database
				- quantity (int OR None): if None : removes the product, otherwise decreases the amount of products in cart.
		"""

		if self.carts[self.osm] is None:
			self.carts[self.osm] = DallizCartController.AVAILABLE_OSMS[self.osm]['class']()

		base_product = cart_content.product

		for osm in DallizCartController.AVAILABLE_OSMS.keys():
			if osm != self.osm:
				equivalent_content = getattr(cart_content, osm+'_content')
				if equivalent_content is not None:
					if quantity is None:
						# Removing completly product from cart
						try:
							equivalent_content.delete()
						except Exception, e:
							connection._rollback()
					else:
						equivalent_product = equivalent_content.product
						equivalent_quantity = self.carts[self.osm].generate_equivalent_quantity(base_product, equivalent_product, quantity)
						if quantity > 0 and equivalent_content.quantity > equivalent_quantity:
							# TO DO : set equivalent quantity
							equivalent_content.quantity = equivalent_content.quantity - equivalent_quantity
							try:
								equivalent_content.save()
							except Exception, e:
								connection._rollback()
						else:
							try:
								equivalent_content.delete()
							except Exception, e:
								connection._rollback()

		self.carts[self.osm].remove(cart_content, quantity)



	def empty(self):
		for osm, cart in self.carts.iteritems():
			if cart:
				cart.empty()

	def get_products_for_export(self, osm):
		"""
		"""
		cart = self.carts[osm]
		products = cart.get_products_for_export()
		return products


	def get_count_summary_products(self):
		"""
			This method returns the count of products that are matched, substituted and missing for each osm.

			Input :
				None
			Return :
				- hash : 
					{
						'osm_name':{
							'substitution': Integer,
							'match': Integer,
							'missing': Integer,
							'count': Integer
						}
					}
		"""

		result = {}
		metacart = self.metacart

		for osm in DallizCartController.AVAILABLE_OSMS.keys():
			cart = getattr(metacart, '%s_cart'%(osm))
			substituted_count = 0
			matched_count = 0
			count = 0
			
			for cart_content in cart.cart_content_set.all():
				count = count + 1
				if cart_content.is_match:
					matched_count = matched_count + 1
				elif cart_content.is_suggested:
					substituted_count = substituted_count + 1

			result[osm] = {
				'substitution' : substituted_count,
				'match' : matched_count,
				'missing': 0,
				'count': count
			}

		# Setting missing count
		osm_max_count = max(result.keys(), key = (lambda key: result[key]['count']))
		max_count = result[osm_max_count]['count']
		[ r.update({'missing': max_count-r['count']})for key, r in result.iteritems()]

		return result