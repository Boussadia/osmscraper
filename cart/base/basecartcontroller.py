#!/usr/bin/python
# -*- coding: utf-8 -*-

class BaseCartController(object):
	"""
		This method acts as a controller on top of a cart entity, it handles adding, removing products to cart as well as computing price of this cart.
		
		Initialisation:
			- CartEntity : cart model entity
			- CartContentEntity : cart content model entity
			- CartHistoryEntity : cart history model entity
			- cart (model of CartEntity) : an already created cart
	"""
	def __init__(self, CartEntity, CartContentEntity, CartHistoryEntity, cart = None):
		self.CartEntity = CartEntity
		self.CartContentEntity = CartContentEntity
		self.CartHistoryEntity = CartHistoryEntity

		if cart is None:
			self.price = 0
			self.cart = self.CartEntity()
			self.cart.save()
		else:
			self.cart = cart
			self.compute_price()

		self.osm = self.cart.osm

	def price(function):
		"""
			This decorator handles price computing. Has to be added to every method that manipulates cart content
		"""
		def wrapper( self , *args, **kwargs) :
			result = function( self , *args, **kwargs)
			self.compute_price()
			return result
		return wrapper

	def compute_price(self):
		self.price = 1
		return self.price

	@price
	def add_product(self, product, quantity = 1):
		if quantity >0:
			content, created = self.cart.cart_content_set.get_or_create( product = product)
			if created:
				content.quantity = quantity
			else:
				content.quantity = content.quantity + quantity 
			content.save()
			return content
		else:
			return None


	@price
	def remove_product(self, product, quantity = None):
		# Getting content of cart
		content = self.cart.cart_content_set.filter(product = product)
		if len(content)>0:
			content = content[0]
		else:
			content = None

		if content is not None:
			if quantity is None:
				# Removing completly product from cart
				content.delete()
			else:
				if quantity > 0 and content.quantity > quantity:
					content.quantity = content.quantity - quantity
					content.save()
				else:
					content.delete()







