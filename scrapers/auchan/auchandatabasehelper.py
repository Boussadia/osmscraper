#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date

from django.db import connection
from django.db import DatabaseError

from scrapers.base.basedatabasehelper import BaseDatabaseHelper

from auchan.models import Category
from auchan.models import Tag
from auchan.models import Brand
from auchan.models import Unit
from auchan.models import Product
from auchan.models import Promotion
from auchan.models import History
from auchan.models import ShippingArea

class AuchanDatabaseHelper(BaseDatabaseHelper):

	def __init__(self):
		super(AuchanDatabaseHelper, self).__init__()

	#-----------------------------------------------------------------------------------------------------------------------
	#
	#									INHERITED METHODS FROM BASE DATABASE HELPER
	#
	#-----------------------------------------------------------------------------------------------------------------------

	def save_categories(self, categories):
		"""
			Method reponsible for saving categories to database.

			Input :
				- categories : list of hash representing categories
		"""

		for main_category in categories:
			main_category_db, created = Category.objects.get_or_create(name = main_category['name'])

			for category_level_1 in main_category['sub_categories']:
				category_level_1_db, created = Category.objects.get_or_create(name = category_level_1['name'], defaults = {'url': category_level_1['url'], 'parent_category': main_category_db})

				if not created:
					category_level_1_db.url = category_level_1['url']
					category_level_1_db.parent_category = main_category_db

				for category_level_2 in category_level_1['sub_categories']:
					category_level_2_db, created = Category.objects.get_or_create(name = category_level_2['name'], defaults = {'url': category_level_2['url'], 'parent_category': category_level_1_db})

					if not created:
						category_level_2_db.url = category_level_2['url']
						category_level_2_db.parent_category = category_level_1_db
		

	def save_products(self, products, parent_category = None, location = None):
		"""
			Method responsible for saving products to database
		"""
		for product in products:
			reference = product['reference']
			url = product['url']

			# Common to product page and category page
			# less detailed information on the product
			if product['is_product']:
				unit = product['unit']
				unit_db, c = Unit.objects.get_or_create(name = unit)
				product_db, created = Product.objects.get_or_create(reference = reference, defaults = {'url': url,'unit': unit_db})
				if not created:
					product_db.url = url
					product_db.unit =  unit_db
					product_db.save()
				if not product['is_promotion']:
					history = History(product = product_db, price = product['price'], unit_price = product['unit_price'], shipping_area = location, availability = product['is_available'])
					history.save()
				if parent_category:
					product_db.categories.add(parent_category)
					# Saving associated tags
					tag, c = Tag.objects.get_or_create(name = product['tag']['name'])
					product_db.tags.add(tag)


			if product['is_promotion']:
				promotion = product['promotion']
				if promotion['type'] == 'multi':
					type = Promotion.MULTI
				elif promotion['type'] == 'simple':
					type = Promotion.SIMPLE
				elif promotion['type'] == 'plus':
					type = Promotion.MORE
				elif promotion['type'] == 'undef':
					type = Promotion.UNDEF

				before = promotion['before']
				after = promotion['after']
				unit_price = promotion['unit_price']

				promotion_db, created = Promotion.objects.get_or_create(reference = reference, shipping_area = location, defaults = {'url': url, 'before':before, 'after':after,'unit_price':unit_price,'type':type, 'availability' : product['is_available']})

				if not created:
					promotion_db.url = url
					promotion_db.before = before
					promotion_db.after = after
					promotion_db.unit_price = unit_price
					promotion_db.type = type
					promotion_db.availability = product['is_available']
					promotion_db.save()

				if product['is_product']:
					promotion_db.content.add(product_db)

			if product['from'] == 'product_page':
				if product['is_product'] and ( not product['is_promotion'] or ( product['is_promotion'] and (product['promotion']['type'] == 'simple' or product['promotion']['type'] == 'plus'))):
					brand, c = Brand.objects.get_or_create(name = product['brand'])
					product_db.brand = brand
					product_db.html = product['html']
					product_db.image_url = product['product_image_url']
					product_db.name = product['name']
					product_db.complement = product['complement']
					# Package
					if product['package'] != {}:
						product_db.package_quantity =product['package']['quantity']
						product_db.package_measure =product['package']['quantity_measure']
						product_db.package_unit =product['package']['unit']

					# Complementary information:
					if 'information' in product and u'Donn\xe9es nutritionnelles' in product['information'][u'Donn\xe9es nutritionnelles']:
						product_db.valeur_nutritionnelle =  product['information'][u'Donn\xe9es nutritionnelles']

					if 'information' in product and u'Avantages' in product['information']:
						product_db.avantages =  product['information'][u'Avantages']

					if 'information' in product and u'Informations pratiques' in product['information']:
						product_db.pratique =  product['information'][u'Informations pratiques']

					if 'information' in product and u'Ingr\xe9dients' in product['information']:
						product_db.ingredients =  product['information'][u'Ingr\xe9dients']

					if 'information' in product and u'Informations de conservation' in product['information']:
						product_db.conservation =  product['information'][u'Informations de conservation']

					product_db.save()
				elif not product['is_product'] and product['is_promotion']:
					if product['promotion']['type'] == 'multi':
						for reference_product in product['promotion']['references']:
							product_in_promotion, created = Product.objects.get_or_create(reference = reference)
							promotion_db.content.add(product_in_promotion)





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
		pass

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
		categories_entities = Category.objects.all()
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
					categories = categories + list(sub_categories)
					continue

		# Organizing categories
		categories = [ {'id': cat.id, 'name': cat.name, 'parent_category_id': cat.parent_category_id, 'url': cat.url, 'db_entity': cat} for cat in categories]

		return categories

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