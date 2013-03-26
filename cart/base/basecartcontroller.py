#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from operator import mul
from copy import deepcopy

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

	def get_promotion_requirement(self, content, base_price):
		"""
			content = [ ( product, quantity)]
		"""
		price = sum( q*p.history_set.all().order_by('-created')[0].price for p,q in content)
		if price>base_price:
			return (False, None)
		elif abs(price -base_price)/base_price<.1:
			return (True, content)
		else:
			for i in xrange(0, len(content)):
				p, q = content[i]
				temp_content = content[::] # Need copy 
				temp_content[i] = p, q+1
				is_ok, new_content = self.get_promotion_requirement(temp_content, base_price)
				if is_ok:
					return (True, new_content)
				else:
					continue
			# Nothing was found, return None
			return (False, None)

	def state_price(self,state):
		"""
			Computes price of state defined as follows:
				state ={
					'products':{product_id:{'price': 3.73, 'qte':10}},
					'promotions':{promotion_id:{'price': 3.73, 'qte':10}},
				}
		"""
		products_price = sum([ state['products'][i]['price']*state['products'][i]['qte'] for i in state['products']])
		promotion_price = sum([ state['promotions'][i]['price']*state['promotions'][i]['qte'] for i in state['promotions']])
		return promotion_price + products_price

	def get_min_state(self, state, requirements, price = None):
		"""
			Computes minumium state for products and multi promotions.

			Example:
				Input : 
					state = {
						'products': {
							1:{'price': 2.13, 'qte':10},
							2:{'price':2.28, 'qte': 5},
							3:{'price': 5, 'qte':3}
						},
						'promotions':{
							1:{'price': 4.26,'qte':0},
							2:{'price': 4.56,'qte':0},
							3:{'price': 4.41,'qte':0},
							4:{'price': 4.56,'qte':0},
						}
					}

					requirements = {
						1:{1:3},
						2:{2:3},
						3:{1:2,2:1},
						4:{1:1,2:2}
					}
				Output :
					finale_state = {
						'products': {
							1: {'price': 2.13, 'qte': 0},
							2: {'price': 2.28, 'qte': 0},
							3: {'price': 5, 'qte': 3}
						},
						'promotions': {
							1: {'price': 4.26, 'qte': 3},
							2: {'price': 4.56, 'qte': 1},
							3: {'price': 4.41, 'qte': 0},
							4: {'price': 4.56, 'qte': 1}
						}
					}
					price = 36.9

		"""
		price_state = self.state_price(state)
		min_state = state
		if price is not None and price_state>price:
			return state, price_state

		if price is None:
			price = price_state

		# Cycling through every promotion and computing state price
		for promotion_id, promotion in state['promotions'].iteritems():
			# Checking if products left:
			products = [ state['products'][i]['qte']>=requirements[promotion_id][i] for i in requirements[promotion_id]]
			if reduce(mul, products):
				# Minimum requirments satisfied
				new_state = deepcopy(state)
				for product_id in requirements[promotion_id]:
					new_state['products'][product_id]['qte'] = new_state['products'][product_id]['qte'] - requirements[promotion_id][product_id]
				new_state['promotions'][promotion_id]['qte'] = new_state['promotions'][promotion_id]['qte'] + 1
				new_price = self.state_price(new_state)
				sub_state, sub_price = self.get_min_state(new_state, requirements, new_price)
				if sub_price<price:
					price = sub_price
					min_state = deepcopy(sub_state)

		return min_state, price

	def get_simple_price(self, content, date = None):
		"""
			Method retrieving product price regardless of promotions

			Input :
				- content : list of cart content model entities
		"""
		prices = []
		for element in content:
			product = element['product']
			quantity = element['quantity']

			history = product.history_set.filter(created__gte = date-timedelta(hours = 24)).order_by('-created')
			if len(history)>0:
				prices.append((element, quantity*history[0].price))
			else:
				history = product.history_set.all().order_by('-created')
				if len(history)>0:
					prices.append((element, quantity*history[0].price))
				else:
					prices.append((element, None))
		return prices

	def compute_price(self, date = None):
		"""
			Method that compuytes price of cart. at a given time.
			Process :
				1 - Go through every product
				2 - Look for pomotions that include a product and the given time
				3 - Add price accordingly

			Input :
				- date : if None, date is now. This is usefull to access evolution of cart price.
		"""
		if date is None:
			date = datetime.now()
		self.price = 0
		# Getting list of product in cart
		content = self.cart.cart_content_set.all()
		# Dictionnary in order to compute minimum state of multi promotion
		state = {
			'products':{},
			'promotions':{}
		}
		requirements = {}

		for element in content:
			p = element.product
			quantity = element.quantity

			# First look for promotion
			simple_promotions = p.promotion_set.filter(end__gte = date, type = 's').distinct('reference', 'end').order_by('-end', 'reference')
			multi_promotions = p.promotion_set.filter(end__gte = date, type = 'm').distinct('reference', 'end').order_by('-end', 'reference')
			if len(simple_promotions)>0:
				promotion = simple_promotions[0]
				self.price = self.price + quantity*promotion.after
			
			elif len(multi_promotions)>0:
				for promotion in multi_promotions:
					price_before = promotion.before
					price_after = promotion.after
					content = [ (p, 1) for p in promotion.content.all()]
					found, requirement = self.get_promotion_requirement(content, price_before)
					requirements[promotion.id] = { p.id:q for p, q in requirement} # updating promotion multi requirements
					# print promotion.url
					# Updating promotion multi state
					prod, price = self.get_simple_price([{'product':p, 'quantity':1}], date)[0]
					# print price
					state['products'][p.id] = {'price': price, 'qte':quantity}
					state['promotions'][promotion.id] = {'price': price_after, 'qte':0}
				# print state

			else:
				history = p.history_set.filter(created__gte = date-timedelta(hours = 24)).order_by('-created')
				if len(history)>0:
					self.price = self.price + quantity*history[0].price
				else:
					history = p.history_set.all().order_by('-created')
					if len(history)>0:
						self.price = self.price + quantity*history[0].price

		# Dealing with multi promotion:
		min_state, min_price = self.get_min_state(state, requirements)
		# print min_state
		self.price = self.price + min_price

		
		# # Taking care of multi promotion
		# for id_promotion, promotion_content in promotions_multi.iteritems():
		# 	promotion =  promotion_content['db_entity']
		# 	# Are all the products found in cart available for promotion?
		# 	required_products = list(promotion.content.all()) # No more than 3 in general
		# 	products_requirement_met = reduce(mul, [(p in required_products) for (p, q) in promotion_content['products_found']])
			
		# 	if products_requirement_met:
		# 		# Computing required product quantities
		# 		price_before = promotion.before
		# 		price_after = promotion.after
		# 		content = [ (p, 1) for p, q in promotion_content['products_found']]
		# 		found, requirement = self.get_promotion_requirement(content, price_before)
		# 		if found:
		# 			# How many promotion do we have ?
		# 			i = 1
		# 			temp_content = promotion_content['products_found'] # Will contain remaining elements
		# 			while 1:
		# 				temp = [ (temp_content[j][0], temp_content[j][1] - requirement[j][1])  for j in xrange(0, len(temp_content))]
		# 				is_positive = reduce(mul, [ (q>=0) for p,q in temp ], 1)
		# 				if not is_positive:
		# 					break
		# 				else:
		# 					temp_content = temp
		# 					i = i+1
		# 			i = i-1 # Number of time promotion is acounted for
		# 			temp_content # Remaining products without promotion

		# 			# Adding promotion price to final price
		# 			self.price = self.price + price_after*i + sum( [ q*p.history_set.all().order_by('-created')[0].price for p,q in temp_content] )

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







