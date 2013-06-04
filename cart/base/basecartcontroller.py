#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import connection, transaction

from copy import deepcopy
from datetime import datetime, timedelta
from operator import mul

from apps.matcher.models import ProductSimilarity, ProductMatch

class BaseCartController(object):
	"""
		This method acts as a controller on top of a cart entity, it handles adding, removing products to cart as well as computing price of this cart.
		
		Initialisation:
			- CartEntity : cart model entity
			- cart (model of CartEntity) : an already created cart
	"""
	def __init__(self, CartEntity, cart = None):
		self.CartEntity = CartEntity

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
			products = [ (i in state['products']) and (state['products'][i]['qte']>=requirements[promotion_id][i]) for i in requirements[promotion_id]]
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
			product = element.product
			quantity = element.quantity

			# First look for promotion
			simple_promotions = product.promotion_set.filter(end__gte = date, type = 's').distinct('reference', 'end').order_by('-end', 'reference')
			multi_promotions = product.promotion_set.filter(end__gte = date, type = 'm').distinct('reference', 'end').order_by('-end', 'reference')
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
					# Updating promotion multi state
					prod, price = self.get_simple_price([{'product':product, 'quantity':1}], date)[0]
					# print quantity
					state['products'][product.id] = {'price': price, 'qte':quantity}
					# print state['products'][product.id]
					state['promotions'][promotion.id] = {'price': price_after, 'qte':0}
			else:
				history = product.history_set.filter(created__gte = date-timedelta(hours = 24)).order_by('-created')
				if len(history)>0:
					self.price = self.price + quantity*history[0].price
				else:
					history = product.history_set.all().order_by('-created')
					if len(history)>0:
						self.price = self.price + quantity*history[0].price

		# Dealing with multi promotion:
		min_state, min_price = self.get_min_state(state, requirements)
		self.price = self.price + min_price

		self.save()

		return self.price

	def save(self, computed = True):
		"""
			Saves price of cart in database.
		"""
		self.cart.cart_history_set.create(price = self.price, computed = computed)

	@price
	def add_product(self, product, quantity = 1, is_user_added = True, is_match = False, is_suggested = False, is_user_set = False, override_qte = False):
		if quantity >0:
			content, created = self.cart.cart_content_set.get_or_create( product = product)
			if created:
				content.quantity = quantity
				content.is_user_added = is_user_added
				content.is_match = is_match
				content.is_suggested = is_suggested
				content.is_user_set = is_user_set
			else:
				if override_qte:
					content.quantity = quantity
				else:
					content.quantity = content.quantity + quantity 
			try:
				content.save()
				return content
			except Exception, e:
				connection._rollback()
				return None
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
				try:
					content.delete()
				except Exception, e:
					connection._rollback()
			else:
				if quantity > 0 and content.quantity > quantity:
					content.quantity = content.quantity - quantity
					try:
						content.save()
					except Exception, e:
						connection._rollback()
				else:
					try:
						content.delete()
					except Exception, e:
						connection._rollback()

	@price
	def empty(self):
		"""
			Empty cart
		"""
		self.cart.products.clear()

	def get_similarites(self, base_product, base_osm):
		return self.similarities(self.osm, base_product, base_osm)

	@staticmethod
	def similarities(index_name, base_product, base_osm):
		"""
			With a product from another osm, get list of similarities.
		"""
		# First get all similarities form tfidf products
		# building args dictionnary to apply to filter, you gotta love Python :D
		kwargs ={
			'query_name': base_osm,
			'index_name': index_name,
			base_osm+'_product': base_product,
			# index_name+'_product__brand__brandmatch__dalliz_brand__in': base_product.brand.brandmatch_set.all(),
			index_name+'_product__dalliz_category__in': base_product.dalliz_category.all(),
		}
		base_tags = base_product.tag.all() # Base products tags
		base_brand = [ bm.dalliz_brand for bm in base_product.brand.brandmatch_set.all()]
		sims = base_product.productsimilarity_set.filter(**kwargs).distinct(index_name+'_product') # Getting similarities
		
		# Computing scores
		scores = [ 
				( 
					getattr(sim, index_name+'_product'),
					10*sum([ 1 for tag in getattr(sim,index_name+'_product').tag.all() if tag in base_tags ]) # Tags score
					+sum([2*sum([ sum([2*(bm.dalliz_brand == dalliz_brand) + 1*( (bm.dalliz_brand != dalliz_brand) and bm.dalliz_brand.is_mdd == dalliz_brand.is_mdd) for dalliz_brand in base_brand]) for bm in brand.brandmatch_set.all()]) for brand in [getattr(sim,index_name+'_product').brand] if brand is not None ]) # brand score
					+ sim.score
				) 

		for sim in sims]

		return sorted((scores), key=lambda item: -item[1])

	def get_equivalent_content(self, base_content, base_osm):
		"""
			This method takes as argument a cart content database entity and its correspondaing osm,
			and returns an equivalent cart content.
		"""
		base_product = base_content.product
		quantity = base_content.quantity
		# First, looking for a match
		match = base_product.productmatch_set.all()
		if len(match)>0:
			match = match[0]
			mathed_product = getattr(match, self.cart.osm+'_product') # Evil hack!! Or is it? I love Python :D
			if mathed_product is not None:
				match_content = self.add_product(mathed_product, quantity, is_user_added = False, is_match = True, is_suggested = False, override_qte = True)
				setattr(match_content, base_content.cart.osm+'_content', base_content)
				setattr(base_content, match_content.cart.osm+'_content', match_content)
				equivalent_content = {
					'content': match_content,
					'is_user_added': False,
					'is_match': True,
					'is_suggested': False
				}

				try:
					base_content.save()
				except Exception, e:
					print e

				try:
					match_content.save()
				except Exception, e:
					print e

				# print '\tMatch : '+mathed_product.url
			else:
				# Look for similarities
				similarities = self.get_similarites(base_product, base_osm)
				if(len(similarities)>0):
					sim_content = self.add_product(similarities[0][0], quantity, is_user_added = False, is_match = False, is_suggested = True, override_qte = True)
					setattr(sim_content, base_content.cart.osm+'_content', base_content)
					setattr(base_content, sim_content.cart.osm+'_content', sim_content)
					equivalent_content = {
						'content': sim_content,
						'is_user_added': False,
						'is_match': False,
						'is_suggested': True
					}
					try:
						base_content.save()
					except Exception, e:
						connection._rollback()

					try:
						sim_content.save()
					except Exception, e:
						connection._rollback()
				else:
					equivalent_content = {
						'content': None,
						'is_user_added': False,
						'is_match': False,
						'is_suggested': True
					}


		else:
			# Look for similarities
			similarities = self.get_similarites(base_product, base_osm)
			if(len(similarities)>0):
				sim_content = self.add_product(similarities[0][0], quantity, is_user_added = False, is_match = False, is_suggested = True, override_qte = True)
				setattr(sim_content, base_content.cart.osm+'_content', base_content)
				setattr(base_content, sim_content.cart.osm+'_content', sim_content)
				equivalent_content = {
					'content': sim_content,
					'is_user_added': False,
					'is_match': False,
					'is_suggested': True
				}
				try:
					base_content.save()
				except Exception, e:
					connection._rollback()

				try:
					sim_content.save()
				except Exception, e:
					connection._rollback()
			else:
				equivalent_content = {
					'content': None,
					'is_user_added': False,
					'is_match': False,
					'is_suggested': True
				}

		return equivalent_content

	def get_content(self, product):
		"""
			Retrieving cart content by product.
		"""
		content = self.cart.cart_content_set.filter(product = product)
		if len(content)>0:
			return content[0]
		return None


	def add_equivalent_content(self, content):
		"""
			Adding directly a cart content to cart.
		"""
		if content['content'] is not None:
			self.cart.cart_content_set.add(content['content'])

	def set_equivalent_cart(self, base_cart):
		"""
			This method computes equivalent cart from an existing cart of another osm.
		"""
		# Emptying cart
		self.empty()

		# Getting base cart content
		contents = base_cart.cart_content_set.all()
		base_osm = base_cart.osm
		equivalence_store = {}

		for content in contents:
			base_product = content.product
			quantity = content.quantity

			# First, looking for a match
			match = base_product.productmatch_set.all()
			if len(match)>0:
				match = match[0]
				mathed_product = getattr(match, self.cart.osm+'_product') # Evil hack!! Or is it? I love Python :D
				if mathed_product is not None:
					match_content = self.add_product(mathed_product, quantity, is_user_added = False, is_match = True, is_suggested = False)
					setattr(match_content, content.cart.osm+'_content', content)
					setattr(content, match_content.cart.osm+'_content', match_content)
					equivalence_store[content] = {
						'content': match_content,
						'is_user_added': False,
						'is_match': True,
						'is_suggested': False
					}

					try:
						content.save()
					except Exception, e:
						print e

					try:
						match_content.save()
					except Exception, e:
						print e

					# print '\tMatch : '+mathed_product.url
				else:
					# Look for similarities
					similarities = self.get_similarites(base_product, base_osm)
					if(len(similarities)>0):
						sim_content = self.add_product(similarities[0][0], quantity, is_user_added = False, is_match = False, is_suggested = True)
						setattr(sim_content, content.cart.osm+'_content', content)
						setattr(content, sim_content.cart.osm+'_content', sim_content)
						equivalence_store[content] = {
							'content': sim_content,
							'is_user_added': False,
							'is_match': False,
							'is_suggested': True
						}
						try:
							content.save()
						except Exception, e:
							connection._rollback()

						try:
							sim_content.save()
						except Exception, e:
							connection._rollback()
					else:
						equivalence_store[content] = {
							'content': None,
							'is_user_added': False,
							'is_match': False,
							'is_suggested': True
						}


			else:
				# Look for similarities
				similarities = self.get_similarites(base_product, base_osm)
				if(len(similarities)>0):
					sim_content = self.add_product(similarities[0][0], quantity, is_user_added = False, is_match = False, is_suggested = True)
					setattr(sim_content, content.cart.osm+'_content', content)
					setattr(content, sim_content.cart.osm+'_content', sim_content)
					equivalence_store[content] = {
						'content': sim_content,
						'is_user_added': False,
						'is_match': False,
						'is_suggested': True
					}
					try:
						content.save()
					except Exception, e:
						connection._rollback()

					try:
						sim_content.save()
					except Exception, e:
						connection._rollback()
				else:
					equivalence_store[content] = {
						'content': None,
						'is_user_added': False,
						'is_match': False,
						'is_suggested': True
					}


		return equivalence_store




