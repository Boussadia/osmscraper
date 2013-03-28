#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta

from django.db import connection
from django.db import DatabaseError
from django.db.models import Q

from scrapers.base.basedatabasehelper import BaseDatabaseHelper
from matcher.monoprix.monoprixstemmer import MonoprixStemmer

from monoprix.models import Category
from monoprix.models import Brand
from monoprix.models import Unit
from monoprix.models import Product
from monoprix.models import Promotion
from monoprix.models import History
from monoprix.models import Store

class MonoprixDatabaseHelper(BaseDatabaseHelper):

	def __init__(self):
		super(MonoprixDatabaseHelper, self).__init__()

	#-----------------------------------------------------------------------------------------------------------------------
	#
	#									INHERITED METHODS FROM BASE DATABASE HELPER
	#
	#-----------------------------------------------------------------------------------------------------------------------

	def save_categories(self, categories, id_parent_category = None):
		"""
			Method reponsible for saving categories to database.

			Input :
				- categories : list of hash representing categories
				- id_parent_category : if not None, this is the id of the parent category in the database.
			Output :
				- list hash representing saved categories (with id and updated time)
		"""
		saved_categories = []
		# print categories
		for i in xrange(len(categories)):
			category = categories[i]
			name = unicode(category['name'])
			url = unicode(category['url'].split(';jsessionid=')[0])
			if id_parent_category:
				category_db, created = Category.objects.get_or_create(url = url, defaults={'name': name, 'parent_category_id': id_parent_category})
			else:
				category_db, created = Category.objects.get_or_create(name = name, defaults={'url': url})

			if not created:
				category_db.name = name
				category_db.parent_category_id = id_parent_category
				category_db.save()

			# Setting id to categories
			category['id'] = category_db.id

			categories[i] = category

		return categories



	def save_products(self, products, id_parent_category = None, location = None):
		"""
			Method responsible for saving products to database

			Input :
				- products : list of hash representing products
				- id_parent_category (int) : id of parent category
				- shipping_area (database entity) : corresponding databse entity
		"""
		# Getting store:
		store = location

		for i in xrange(0, len(products)):
			try:
				product = products[i]
				if 'exists' in product and not product['exists']:
					# Product does not exist, set it in database
					product_db = Product.objects.filter(reference = product['reference'])
					if len(product_db)>0:
						product_db = product_db[0]
						product_db.exists = False
						product_db.save()
					else:
						promotion_db = Promotion.objects.filter(reference = product['reference'])
						if len(promotion_db)>0:
							promotion_db = promotion_db[0]
							promotion_db.availability = False
							promotion_db.save()

					return []
				else:
					exists = True

				availability = product['is_available']

				if not availability:
					reference = product['reference']

					# Getting product from database, and saving history indicating non availability
					product = Product.objects.filter(reference = reference)
					if len(product):
						product = product[0]
						history = History(product = product, availability = False, store = store)
						history.save()
						return


				# Common
				reference = product['reference']
				name = product['name']
				url = product['url'].split(';jsessionid=')[0]
				html = product['html']
				if 'parent_brand' in product:
					parent_brand = product['parent_brand']
				else:
					parent_brand = None

				if 'brand' in product and product['brand'] != '' and parent_brand is not None:
					brand = self.save_brand(product['brand'], parent_brand = parent_brand)
				else:
					brand = None

				if 'unit' in product and product['unit'] != '':
					unit = self.save_unit(product['unit'])
				else:
					unit = None

				image_url = product['product_image_url'].split(';jsessionid=')[0]

				# Promotion specific
				if product['is_promotion']:
					after = product['promotion']['after']
					before = product['promotion']['before']
					unit_price = product['promotion']['unit_price']
					if 'date_start' in product['promotion'] and 'date_end' in product['promotion']:
						start = date(year = int(product['promotion']['date_start']['year']), month = int(product['promotion']['date_start']['month']), day = int(product['promotion']['date_start']['day']))
						end = date(year = int(product['promotion']['date_end']['year']), month = int(product['promotion']['date_end']['month']), day = int(product['promotion']['date_end']['day']))
					else:
						start = None
						end = None

				if product['is_product']:
					# Detailed information
					if 'information' in product and u'Description' in product['information']:
						description = product['information'][u'Description']
					else:
						description = None
					#
					if 'information' in product and u'Conservation' in product['information']:
						conservation = product['information'][u'Conservation']
					else:
						conservation = None

					if 'information' in product and u"Conseil" in product['information']:
						conseil = product['information'][u"Conseil"]
					else:
						conseil = None
					# done
					if 'information' in product and u'Ingrédients' in product['information']:
						ingredients = product['information'][u'Ingrédients']
					else:
						ingredients = None

					if 'information' in product and u'Composition' in product['information']:
						composition = product['information'][u'Composition']
					else:
						composition = None
					#
					if 'information' in product and u'Valeur nutritionnelle' in product['information']:
						valeur_nutritionnelle = product['information'][u'Valeur nutritionnelle']
					else:
						valeur_nutritionnelle = None

					# Package
					if 'package' in product and 'unit' in product['package']:
						package_unit = product['package']['unit']
					else:
						package_unit = None

					if 'package' in product and 'quantity_measure' in product['package']:
						package_measure = float(product['package']['quantity_measure'])
					else:
						package_measure = None

					if 'package' in product and 'quantity' in product['package']:
						package_quantity = int(product['package']['quantity'])
					else:
						package_quantity = None

					# Saving product to database
					product_db, created = Product.objects.get_or_create(reference = reference, defaults={
						'name': name,
						'url': url,
						'image_url': image_url,
						'unit': unit,
						'description': description,
						'ingredients': ingredients,
						'valeur_nutritionnelle': valeur_nutritionnelle,
						'conservation': conservation,
						'conseil': conseil,
						'composition': composition,
						'package_unit': package_unit,
						'package_quantity': package_quantity,
						'package_measure': package_measure,
						'exists': exists
						})

					if not created:
						product_db.name = name
						product_db.url = url
						product_db.reference = reference
						product_db.unit = unit
						product_db.description = description
						product_db.ingredients = ingredients
						product_db.valeur_nutritionnelle = valeur_nutritionnelle
						product_db.conservation = conservation
						product_db.conseil = conseil
						product_db.composition = composition
						product_db.package_unit = package_unit
						product_db.package_quantity = package_quantity
						product_db.package_measure = package_measure
						product_db.exists = exists
						product_db.save()

					if brand is not None:
						product_db.brand = brand
						product_db.save()


					# Do we need to save the html in the product?
					if 'information' in product:
						product_db.html = html
						product_db.stemmed_text = MonoprixStemmer(html).stem_text()
						product_db.save()

					# Adding category to Product
					if id_parent_category:
						categories = product_db.categories.all()
						cat = Category.objects.filter(id = id_parent_category)
						if len(cat) == 1:
							cat = cat[0]
							if created:
								[[product_db.tag.add(t) for t in c.tags.all()] for c in cat.dalliz_category.all()]
							if cat not in categories:
								product_db.categories.add(cat)
								[product_db.dalliz_category.add(c) for c in cat.dalliz_category.all()]

					if not product['is_promotion']:
						# Saving image
						product_db.image_url = image_url
						product_db.save()

						# Prices for history
						price = product['price']
						unit_price = product['unit_price']

						# Saving history to database
						history = History(product = product_db, price = price, unit_price = unit_price, availability = availability, html = html, store = store)
						history.save()

					elif product['promotion']['type'] == 'simple':
						# Simple promotion
						promotion, created = Promotion.objects.get_or_create(reference = reference, defaults = {'type': Promotion.SIMPLE, 'url': url, 'image_url': image_url, 'before': before, 'after': after, 'unit_price': unit_price, 'start': start, 'end': end, 'store': store, 'availability': availability, 'html': html})
						if created:
							promotion.type = Promotion.SIMPLE
							promotion.url = url
							promotion.image_url= image_url
							promotion.before = before
							promotion.after = after
							promotion.unit_price = unit_price
							promotion.start = start
							promotion.end = end
							promotion.store = store
							promotion.availability = availability
							promotion.html =  html
							promotion.save()
						promotion.content.add(product_db)
				elif product['is_product'] == False and product['is_promotion'] and product['promotion']['type'] == 'multi':
					# Multi promotion
					promotion, created = Promotion.objects.get_or_create(reference = reference, store = store, defaults = {'type': Promotion.MULTI, 'url': url, 'image_url': image_url, 'before': before, 'after': after, 'unit_price': unit_price, 'start': start, 'end': end, 'availability': availability, 'html': html})
					if created:
						promotion.type = Promotion.MULTI
						promotion.url = url
						promotion.image_url= image_url
						promotion.before = before
						promotion.after = after
						promotion.unit_price = unit_price
						promotion.start = start
						promotion.end = end
						promotion.availability = availability
						promotion.html =  html
						promotion.save()
					# Adding content of package
					if 'references' in product['promotion']:
						for reference in product['promotion']['references']:
							# Is there a product with reference?
							content_product = Product.objects.filter(reference = reference)
							if len(content_product)>0:
								content_product = content_product[0]
							else:
								content_product = Product(reference = reference)
								content_product.save()
							promotion.content.add(content_product)
			except DatabaseError, e:
				connection._rollback()
				print 'Failed to save product to database %s'%(e)
				print product, id_parent_category, store
				raise e
			

	def save_brand(self, brand_name, parent_brand = None):
		"""
			Saves and return brand entity.
		"""
		if parent_brand is not None or parent_brand != '':
			parent_brand, created = Brand.objects.get_or_create(name = unicode(parent_brand.strip()))
			return parent_brand


	def save_unit(self, unit_name):
		"""
			Saves and return unit entity.
		"""
		if unit_name:
			unit, created = Unit.objects.get_or_create(name = unicode(unit_name))
			return unit
		else:
			return None

	def get_products(self, options = {}):
		"""
			Method responsible for retireving products from database.

			Input :
				- option (hash) : 
					1. {
						'type': 'single',
						'filter':{
							'reference': '...' (optional)
							'image_url': '...',(optional, if reference is not set),
						}
					}
					2. {
						'type': 'multi',
						'filter': {
							'after_date': 'datetime' (optional retrieve products updated after date),
							'before_date': 'datetime' (optional retrieve products older than date),
							'category_id': id (optional)
						}
					}
			Output : 
				- list of products (represented by hash)
		"""
		products = Product.objects.all()
		if 'reference' in options:
			product_db = Product.objects.filter(reference = options['reference'])
			if len(product_db) == 1:
				product_db = product_db[0]
				return [self.serialize(product)]


		if 'categories_id' in options:
			products = Product.objects.filter(categories__id__in = options['categories_id'])
		
		if 'locations' in options:
			products = products.filter(history__store__postal_code__in = [l['postal_code'] for l in options['locations']])

		if 'before_date' in options:
			products = products.filter(history__created__lte = options['before_date'])

		products = products.filter(exists = True)

		products = self.serialize(products)
		# Getting locations of all products
		[ p.update({'locations' : [{'id':s.id,'name': s.name, 'postal_code':s.postal_code, 'city_name':s.city_name, 'address':s.address, 'is_LAD': s.is_LAD} for s in list(Store.objects.filter(history__product__id = p['id']))]}) for p in products]

		return products

	def get_uncomplete_products(self):
		"""
			This method retrieves products and promotion hat are not complete

			- Output :
				- products : [{'url':...}]
		"""
		# Getting products first, defined by : all informations fields are null and was created less than a month ago
		products = Product.objects.filter(exists = True, created__gte=datetime.today() - timedelta(days = 30)) # filter by date
		# products = products.filter(url__isnull = False, origine__isnull=True, informations__isnull=True, ingredients__isnull=True,conservation__isnull=True,avertissements__isnull=True, composition__isnull=True,conseils__isnull=True)
		products = products.filter(url__isnull = False, exists = True, html__isnull=True)
		products = [{'url' :p.url} for p in products]

		# Getting promotions : defined by start and end date of promotion are null
		promotions_db = Promotion.objects.filter(Q(start__isnull = True)|Q(end__isnull = True), Q(availability = True))
		promotions = [{'url' :p.url, 'location' : p.shipping_area.postal_code} for p in promotions_db if p.shipping_area is not None]
		promotions = promotions+[{'url' :p.url} for p in promotions_db if p.shipping_area is None]

		return promotions + products

	def get_categories(self, options = {}):
		"""
			Method that retrieves all categories in a hash.

			Input:
				- option (hash) : 
					1. {
						'leaves' : boolean, get categories with no childs (optional),
						'id_parent_category': id of parent category (optional),
						'url': url of category (optionnal)
						'start_date':  (datetime) retireve category updated after this date (optional),
						'end_date':  (datetime) retireve category updated before this date (optional),
					}

			Output :
				- categories : list of hashs representing categories.
		"""
		categories_entities = Category.objects.filter(exists = True)
		if 'id_parent_category' in options and options['id_parent_category']:
			id_parent_category = options['id_parent_category']
			categories_entities = categories_entities.filter(parent_category_id = id_parent_category)

		if 'url' in options and options['url']:
			url = options['url']
			categories_entities = categories_entities.filter(url = url)

		if 'start_date' in options and options['start_date']:
			start_date = options['start_date']
			categories_entities = categories_entities.filter(updated__gte=start_date)

		if 'end_date' in options and options['end_date']:
			end_date = options['end_date']
			categories_entities = categories_entities.filter(updated__lte=end_date)

		categories = list(categories_entities)

		if 'leaves' in options and options['leaves']:
			# Keeping only category leaves, i.e. category that are not parent of another category
			# if a parent category is in categories_entities, remove it but get its children
			i = 0
			while i<len(categories):
				category = categories[i]
				sub_categories = Category.objects.filter(parent_category = category)
				if len(sub_categories) == 0:
					# This category is a leaf keep going
					i = i+1
					continue
				else:
					# This is not a leaf, remove it and add sub categories to end of list
					categories.pop(i)
					categories = categories + filter(lambda sub_cat:sub_cat not in categories, list(sub_categories))
					continue

		# Organizing categories
		categories = [ {'id': cat.id, 'name': cat.name, 'parent_category_id': cat.parent_category_id, 'url': cat.url, 'updated': cat.updated, 'db_entity': cat} for cat in categories]


		return categories

	def save_stores(self, stores):
		"""
			Method that handle stores saving

			Input :
				- stores (list of hash) :
					[{
						'id':..., # Optionnal
						'name': ...,
						'city_name': ...,
						'postal_code': ...,
						'address': ...,
						'is_LAD': ...
					}]
		"""

		for store in stores:
			city_name = store['city_name']
			postal_code = store['postal_code']
			is_LAD = store['is_LAD']
			name = store['name']

			if 'id' in store:
				store_db = Store.objects.filter(id = store['id'])
				if len(store_db) == 1:
					store_db = store_db[0]
					store_db.city_name = store['city_name']
					store_db.postal_code = store['postal_code']
					store_db.is_LAD = store['is_LAD']
					store_db.name = store['name']
					store_db.save()
			else:
				store_db, created = Store.objects.get_or_create(postal_code = postal_code,city_name = city_name, address = address, name = name, defaults={ 'is_LAD': is_LAD})
				if not created:
					store_db.is_LAD = is_LAD
					store_db.save()

	def get_stores(self):
		"""
			Get from database all Monoprix get_stores

			Output :
				- list of hash : [{
					'id':...,
					'name': ...,
					'city_name': ...,
					'postal_code': ...,
					'address': ...,
					'is_LAD': ...
				}]
		"""
		stores = Store.objects.all()

		stores_return = [{'id':s.id,'name': s.name, 'postal_code':s.postal_code, 'city_name':s.city_name, 'address':s.address, 'is_LAD': s.is_LAD} for s in stores]

		return stores_return

	def get_store(self, location):
		"""
			Extract store form database.

			Input :
				- location {
					'name': ...,
					'city_name': ...,
					'postal_code': ...,
					'address': ...,
				}
		"""

		store = Store.objects.filter(postal_code = location['postal_code'])

		if len(store) == 1:
			return store[0]
		elif len(store) == 0:
			return None
		else:
			store = Store.objects.filter(postal_code = location['postal_code'], city_name = location['city_name'])

			if len(store) == 1:
				return store[0]
			elif len(store) == 0:
				return None
			else:
				store = Store.objects.filter(postal_code = location['postal_code'], city_name = location['city_name'], address = location['address'])
				if len(store) > 0:
					return store[0]
				else:
					return None




