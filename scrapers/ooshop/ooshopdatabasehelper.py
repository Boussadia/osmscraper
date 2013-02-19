#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
import simplejson as json

from django.db import connection
from django.db import DatabaseError
from django.db.models import Q

from django.conf import settings
from django.core import serializers


from scrapers.base.basedatabasehelper import BaseDatabaseHelper

from ooshop.models import Category
from ooshop.models import NewBrand as Brand
from ooshop.models import Unit
from ooshop.models import NewProduct as Product
from ooshop.models import Promotion
from ooshop.models import History
from ooshop.models import ShippingArea

class OoshopDatabaseHelper(BaseDatabaseHelper):

	def __init__(self):
		super(OoshopDatabaseHelper, self).__init__()

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
			url = unicode(category['url'])
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



	def save_products(self, products, id_parent_category, shipping_area = None):
		"""
			Method responsible for saving products to database

			Input :
				- products : list of hash representing products
				- id_parent_category (int) : id of parent category
				- shipping_area (database entity) : corresponding databse entity
		"""
		for i in xrange(0, len(products)):
			# try:
			product = products[i]

			if 'exists' in product and not product['exists'] and shipping_area is None:
				# Product does not exist, set it in database
				product_db = Product.objects.filter(reference = product['reference'])
				if len(product_db)>0:
					product_db = product_db[0]
					product_db.exists = False
					product_db.save()

				return []

			# Common
			reference = product['reference']
			url = product['url']
			if 'name' in product:
				name = product['name']
			else:
				name = None

			if 'html' in product:
				html = product['html']
			else:
				html = None

			if 'brand' in product and product['brand'] != '':
				brand = self.save_brand(product['brand'], product['brand_image_url'])
			else:
				brand = None

			if 'unit' in product and product['unit'] != '':
				unit = self.save_unit(product['unit'])
			else:
				unit = None

			if 'product_image_url' in product:
				image_url = product['product_image_url']
			else:
				image_url = None
			availability = product['is_available']

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
				informations = None
				conservation = None
				conseils = None
				origine = None
				ingredients = None
				composition = None
				avertissements = None
				if 'information' in product:
					for key in product['information'].keys():
						if 'information' in key.lower():
							informations = product['information'][key]
						elif 'conservation' in key.lower():
							conservation = product['information'][key]
						elif 'origin' in key.lower():
							origine = product['information'][key]
						elif u"conseils d'utilisation" in key.lower():
							conseils = product['information'][key]
						elif u'ingrédients' in key.lower():
							ingredients = product['information'][key]
						elif 'composition' in key.lower():
							composition = product['information'][key]
						elif 'avertissements' in key.lower():
							avertissements = product['information'][key]

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
				if image_url:
					product_db, created = Product.objects.get_or_create(image_url = image_url, defaults={
						'name': name,
						'url': url,
						'reference': reference,
						'brand': brand,
						'unit': unit,
						'informations': informations,
						'conservation': conservation,
						'origine': origine,
						'conseils': conseils,
						'ingredients': ingredients,
						'composition': composition,
						'avertissements': avertissements,
						'package_unit': package_unit,
						'package_quantity': package_quantity,
						'package_measure': package_measure
						})
				else:
					product_db, created = Product.objects.get_or_create(reference = reference, defaults={
						'name': name,
						'url': url,
						'image_url': image_url,
						'brand': brand,
						'unit': unit,
						'informations': informations,
						'conservation': conservation,
						'origine': origine,
						'conseils': conseils,
						'ingredients': ingredients,
						'composition': composition,
						'avertissements': avertissements,
						'package_unit': package_unit,
						'package_quantity': package_quantity,
						'package_measure': package_measure
						})

				if not created:
					product_db.name = name
					product_db.url = url
					product_db.reference = reference
					product_db.image_url = image_url
					product_db.brand = brand
					product_db.unit = unit
					product_db.informations = informations
					product_db.conservation = conservation
					product_db.origine = origine
					product_db.conseils = conseils
					product_db.ingredients = ingredients
					product_db.composition = composition
					product_db.avertissements = avertissements
					product_db.package_unit = package_unit
					product_db.package_quantity = package_quantity
					product_db.package_measure = package_measure
					product_db.save()

				# Do we need to save the html in the product?
				if 'information' in product:
					product_db.html = html
					product_db.save()

				# Adding category to Product
				if id_parent_category:
					cat = Category.objects.filter(id = id_parent_category)
					if len(cat) == 1:
						product_db.categories.add(cat[0])

				if not product['is_promotion']:
					# Saving image
					product_db.image_url = image_url
					product_db.save()

					# Prices for history
					price = product['price']
					unit_price = product['unit_price']

					# Saving history to database
					history = History(product = product_db, price = price, unit_price = unit_price, availability = availability, html = html, shipping_area = shipping_area)
					history.save()

					# Is it a goodie?
					if price == 0 and product_db.goodie == False:
						product_db.goodie = True
						product_db.save()
				elif product['promotion']['type'] == 'simple':
					# Simple promotion
					promotion, created = Promotion.objects.get_or_create(reference = reference, shipping_area = shipping_area, defaults = {'type': Promotion.SIMPLE, 'url': url, 'image_url': image_url, 'before': before, 'after': after, 'unit_price': unit_price, 'start': start, 'end': end, 'availability': availability, 'html': html})
					if not created:
						promotion.type = Promotion.SIMPLE
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
					promotion.content.add(product_db)
			elif product['is_product'] == False and product['is_promotion'] and product['promotion']['type'] == 'multi':
				# Multi promotion
				promotion, created = Promotion.objects.get_or_create(reference = reference, shipping_area = shipping_area, defaults = {'type': Promotion.MULTI, 'url': url, 'image_url': image_url, 'before': before, 'after': after, 'unit_price': unit_price, 'start': start, 'end': end, 'availability': availability, 'html': html})
				if not created:
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
				if 'product_image_urls' in product['promotion']:
					for product_image_url in product['promotion']['product_image_urls']:
						# Is there a product with this image url?
						content_product = Product.objects.filter(image_url = product_image_url)
						if len(content_product)>0:
							content_product = content_product[0]
						else:
							content_product = Product(image_url = product_image_url)
							content_product.save()
						promotion.content.add(content_product)
			# except DatabaseError, e:
			# 	connection._rollback()
			# 	print 'Failed to save product to database %s'%(e)
			# 	print product, id_parent_category, shipping_area
			# 	raise e
			

	def save_brand(self, brand_name, brand_image_url):
		"""
			Saves and return brand entity.
		"""
		brand, created = Brand.objects.get_or_create(name = brand_name, defaults = {'image_url': brand_image_url})
		if not created:
			brand.image_url = brand_image_url
			brand.save()
		return brand

	def save_unit(self, unit_name):
		"""
			Saves and return unit entity.
		"""
		if unit_name:
			unit, created = Unit.objects.get_or_create(name = unit_name)
			return unit
		else:
			return None

	def get_products(self, options = {}):
		"""
			Method responsible for retireving products from database.

			Input :
				- option (hash) : 
					1. {
						'reference': '...' (optional)
						'image_url': '...',(optional, if reference is not set),
					}
					2. {
						'after_date': 'datetime' (optional retrieve products updated after date),
						'before_date': 'datetime' (optional retrieve products older than date),
						'categories_id': list of ids id (optional),
						'locations': list of locations...
					}
			Output : 
				- list of products (represented by hash)
		"""
		products = []
		if 'reference' in options:
			product_db = Product.objects.filter(reference = options['reference'])
			if len(product_db) == 1:
				product_db = product_db[0]
				return [self.serialize(product)]


		if 'categories_id' in options:
			products = Product.objects.filter(categories__id__in = options['categories_id'])
		
		if 'locations' in options:
			products = products.filter(history__shipping_area__postal_code__in = options['locations'])

		if 'before_date' in options:
			products = products.filter(history__created__lte = options['before_date'])

		products = self.serialize(products)
		# Getting locations of all products and 
		[ p.update({'locations' : [s.postal_code for s in list(ShippingArea.objects.filter(history__product__id = p['id']))]}) for p in products]

		return products

	def get_uncomplete_products(self):
		"""
			This method retrieves products and promotion hat are not complete

			- Output :
				- products : [{'url':...}]
		"""
		# Getting products first, defined by : all informations fields are null and was created less than a month ago
		products = Product.objects.filter(created__gte=datetime.today() - timedelta(days = 30)) # filter by date
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
						'start_date':  (datetime) retireve category updated after this date (optional),
						'end_date':  (datetime) retireve category updated before this date (optional),
					}

			Output :
				- categories : list of hashs representing categories.
		"""
		categories_entities = Category.objects.all()
		if 'id_parent_category' in options and options['id_parent_category']:
			id_parent_category = options['id_parent_category']
			categories_entities = categories_entities.filter(parent_category_id = id_parent_category)

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
		categories = [ {'id': cat.id, 'name': cat.name, 'parent_category_id': cat.parent_category_id, 'url': cat.url, 'updated': cat.updated} for cat in categories]

		return categories

	def get_category_by_url(self, category_url):
		"""
			Getting category entity from database with category_url

			Input :
				- category_url (string) : url of category page
			Output : 
				- category model entity if exists, None otherwise
		"""
		category = Category.objects.filter(url = category_url)
		if len(category) == 0:
			return None
		else:
			return category[0]


	def get_shipping_areas(self):
		"""
			Method reponsible for retrieving shipping areas

			Output :
				- list of hash : {'id':..., 'city_name': ..., 'postal_code': .....}
		"""
		shipping_areas = ShippingArea.objects.all()
		return self.serialize(shipping_areas)

	def get_shipping_area(self, location):
		"""
			Method reponsible for retrieving shipping areas

			Output :
				- location = postal code
		"""

		shipping_area = ShippingArea.objects.filter(postal_code = location, is_shipping_area = True)

		if len(shipping_area) > 0:
			return shipping_area[0]
		elif len(shipping_area) == 0:
			return None

	def save_shipping_areas(self, shipping_areas):
		"""
			Method that handle shipping areas saving

			Input :
				- shipping_area (list of hash) : {'city_name': ..., 'postal_code': ....., 'is_shipping_area': Bool}
		"""

		for shipping_area in shipping_areas:
			city_name = shipping_area['name']
			postal_code = shipping_area['postal_code']
			is_shipping_area = shipping_area['is_shipping_area']
			area, created = ShippingArea.objects.get_or_create(postal_code = postal_code,city_name = city_name, defaults={ 'is_shipping_area': is_shipping_area})
			if not created:
				area.city_name = city_name
				area.is_shipping_area = is_shipping_area
				area.save()

	def empty_database(self):
		"""
			This method is only for developement purposes, DO NOT EXECUTE ON PRODUCTION WHEN DEBUG = False!!!
			IF YOU DO THAT I WILL LOOK FOR YOU, I WILL FIND YOU, AND I WILL KILL YOU! (http://www.youtube.com/watch?v=1SXsCkKuvOU)
		"""
		if settings.DEBUG:
			answer = raw_input("ARE YOU SURE? (YES DALLIZ-> yes, anything else ->no): ")
			if answer == 'YES DALLIZ':
				print 'Deleting'
				Category.objects.all().delete()
				History.objects.all().delete()
				Promotion.objects.all().delete()
				Product.objects.all().delete()

			else:
				print 'Aborted'
		else:
			print 'YOU ARE SO DUMB, YOU ARE REALLY DUMB, FOR REAL! (http://www.youtube.com/watch?v=bobp5OHVsWY) (DEBUG = False -> production server)'

