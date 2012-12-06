#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.mail import send_mail

from scrapers.ooshop import Ooshop
from models import *

ooshop = Ooshop()

def save_categories(categories):
	"""
		Saving ooshop categories.

		Input:
			- categories : list of categories ooshop
	"""

	sub_categories_final_list = []

	for main_category_name, main_category_content in categories.iteritems():
		url = main_category_content['url']
		sub_categories = main_category_content['sub_categories']
		main_category_db, created = Category_main.objects.get_or_create(name=unicode(main_category_name), defaults={'url': unicode(url)})
		
		if created:
			print 'New main category %s saved in database'%(main_category_name)
		else:
			print 'Main category %s updated in database'%(main_category_name)

		# Saving sub categories

		for sub_category_name, sub_category_content in sub_categories.iteritems():
			url_sub_category = sub_category_content['url']
			cookie_sub_category = sub_category_content['cookie']
			sub_categories_level_2 = sub_category_content['sub_categories']
			sub_category_db, created = Category_sub_level_1.objects.get_or_create(name = unicode(sub_category_name),parent_category = main_category_db, defaults={'url': unicode(url_sub_category), 'cookie': unicode(cookie_sub_category)})
			if created:
				print 'New sub category %s saved in database'%(sub_category_name)
			else:
				sub_category_db.url = url_sub_category
				sub_category_db.cookie = cookie_sub_category
				sub_category_db.save()
				print 'Sub category %s updated in database'%(sub_category_name)

			if len(sub_categories_level_2)>0:
				for sub_category_level_2_name, sub_category_level_2_content in sub_categories_level_2.iteritems():
					url_sub_category_level_2 = sub_category_level_2_content['url']
					cookie_sub_category_level_2 = sub_category_level_2_content['cookie']
					sub_categories_level_3 = sub_category_level_2_content['sub_categories']
					sub_category_level_2_db, created = Category_sub_level_2.objects.get_or_create(name = unicode(sub_category_level_2_name),parent_category = sub_category_db, defaults={'url': unicode(url_sub_category_level_2), 'cookie': unicode(cookie_sub_category_level_2)})

					if created:
						print 'New sub category level 2 %s saved in database'%(sub_category_level_2_name)
					else:
						sub_category_level_2_db.url = url_sub_category_level_2
						sub_category_level_2_db.cookie = cookie_sub_category_level_2
						sub_category_level_2_db.save()
						print 'Sub category level 2 %s updated in database'%(sub_category_level_2_name)

				if len(sub_categories_level_3)>0:
					for sub_category_final_name, sub_category_final_content in sub_categories_level_3.iteritems():
						url_sub_category_final = sub_category_final_content['url']
						cookie_sub_category_final = sub_category_final_content['cookie']
						sub_category_final_db, created = Category_final.objects.get_or_create(name = unicode(sub_category_final_name),parent_category = sub_category_level_2_db, defaults={'url': unicode(url_sub_category_final), 'cookie': unicode(cookie_sub_category_final)})
						sub_categories_final_list.append(sub_category_final_db)

						if created:
							print 'New sub category level 3 %s saved in database'%(sub_category_final_name)
						else:
							sub_category_final_db.url = url_sub_category_final
							sub_category_final_db.cookie = cookie_sub_category_final
							sub_category_final_db.save()
							print 'Sub category level 3 %s updated in database'%(sub_category_final_name)
				else:
					print 'No sub categories level 3 for sub category %s'%(sub_category_level_2_name)
					sub_category_final_db, created = Category_final.objects.get_or_create(name = unicode(sub_category_level_2_name),parent_category = sub_category_level_2_db, defaults={'url': unicode(url_sub_category_level_2), 'cookie': unicode(cookie_sub_category_level_2)})
					if not created:
						sub_category_final_db.url = url_sub_category_level_2
						sub_category_final_db.cookie = cookie_sub_category_level_2
						sub_category_final_db.save()
					sub_categories_final_list.append(sub_category_final_db)


			else:
				print 'No sub categories level 2 for sub category %s'%(sub_category_name)
				sub_category_level_2_db, created = Category_sub_level_2.objects.get_or_create(name = unicode(sub_category_name),parent_category = sub_category_db, defaults={'url': unicode(url_sub_category), 'cookie': unicode(cookie_sub_category)})
				if not created:
					sub_category_level_2_db.url = url_sub_category
					sub_category_level_2_db.cookie = cookie_sub_category
					sub_category_level_2_db.save()
				sub_category_final_db, created = Category_final.objects.get_or_create(name = unicode(sub_category_name),parent_category = sub_category_level_2_db, defaults={'url': unicode(url_sub_category), 'cookie': unicode(cookie_sub_category)})
				if not created:
					sub_category_final_db.url = url_sub_category
					sub_category_final_db.cookie = cookie_sub_category
					sub_category_final_db.save()
				sub_categories_final_list.append(sub_category_final_db)

	return sub_categories_final_list

def save_products(final_categories):
	for i in xrange(0, len(final_categories)):
		category = {
			'url': final_categories[i].url,
			'name': final_categories[i].name,
			'cookie': final_categories[i].cookie
		}

		products = ooshop.get_products_for_category(category)

		for i in xrange(0, len(products)):
			save_product(products[i], final_categories[i])

def save_product(product, final_category):
	"""
		Saving product to database

		Input :
			- product : hash representing a product parsed from html
			- final_category : database entity representing category of product
	"""
	# Saving brand
	brand = product['brand']
	brand_db = save_brand(brand)

	# Saving Unit
	unit = product['unit']
	unit_db = save_unit(unit)

	# Saving product
	reference = product['reference']
	title = product['name']
	url = product['url']
	image_url = product['image_url']

	product_db, created = Product.objects.get_or_create(reference = unicode(reference), defaults = {'title': unicode(title), 'url': unicode(url), 'image_url': unicode(image_url), 'unit_id': unit_db.id, 'brand_id': brand_db.id})

	if created:
		print 'Created product '+title
	else:
		print 'Updating product '+title
		product_db.title = title
		product_db.image_url = image_url
		product_db.url = url
		product_db.brand = brand_db
		product_db.unit = unit_db
		product_db.save()

	# Adding category
	product_db.category.add(final_category)

	# Saving history
	price = product['price']
	unit_price = product['unit_price']
	promotion = product['promotion']

	product_history = Product_history(product = product_db, price = price, unit_price = unit_price, promotion_type = promotion['type'], promotion = 0)

	if promotion['type'] == 'simple' or promotion['type'] == 'lot':
		product_history.promotion = promotion['percentage']
	product_history.save()

	# If type of promoption is a combination of product : add them
	if promotion['type'] == 'lot':
		for j in xrange(0, len(promotion['references'])):
			reference = promotion['references'][j]
			ref_product, created = Product.objects.get_or_create(reference = reference)
			product_history.references.add(ref_product)

def save_brand(brand_name):
	brand_db, created = Brand.objects.get_or_create(name = unicode(brand_name) )
	return brand_db

def save_unit(unit_name):
	unit_db, created = Unit.objects.get_or_create(name = unicode(unit_name ))
	return unit_db



def perform_complete_scraping():
	ooshop.get_menu()
	categories = ooshop.get_categories()
	sub_categories_final_list = save_categories(categories)
	save_products(sub_categories_final_list)

