#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import # Import because of modules names

import pystache
import simplejson as json
import hashlib
from time import time
import re
import itertools

from osmscraper.unaccent import unaccent

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from tags.models import Tag

from ooshop.models import Category as OoshopCategory
from monoprix.models import Category as MonoprixCategory
from auchan.models import Category as AuchanCategory
from dalliz.models import Category as DallizCategory
from ooshop.models import NewProduct as OoshopProduct
from monoprix.models import NewProduct as MonoprixProduct
from auchan.models import Product as AuchanProduct
from matcher.models import ProductSimilarity
from matcher.models import ProductMatch



available_osms = {
	'auchan':{
		'category': AuchanCategory,
		'product': AuchanProduct,
		'query':{
			'ooshop':lambda p: [serialize_product(sim.ooshop_product, 'ooshop') for sim in ProductSimilarity.objects.filter(index_name = 'ooshop', query_name = 'auchan', auchan_product__id = p['id'], auchan_product__brand__brandmatch__dalliz_brand = p['dalliz_brand']).order_by('-score')[:1]],
			'monoprix':lambda p: [serialize_product(sim.monoprix_product, 'monoprix') for sim in ProductSimilarity.objects.filter(index_name = 'monoprix', query_name = 'auchan', auchan_product__id = p['id'], auchan_product__brand__brandmatch__dalliz_brand = p['dalliz_brand']).order_by('-score')[:1]],
		}
	},
	'monoprix':{
		'category': MonoprixCategory,
		'product': MonoprixProduct,
		'query':{
			'auchan':lambda p: [serialize_product(sim.auchan_product, 'auchan') for sim in ProductSimilarity.objects.filter(index_name = 'auchan', query_name = 'monoprix', monoprix_product__id = p['id'], monoprix_product__brand__brandmatch__dalliz_brand = p['dalliz_brand']).order_by('-score')[:1]],
			'ooshop':lambda p: [serialize_product(sim.ooshop_product, 'ooshop') for sim in ProductSimilarity.objects.filter(index_name = 'ooshop', query_name = 'monoprix', monoprix_product__id = p['id'], monoprix_product__brand__brandmatch__dalliz_brand = p['dalliz_brand']).order_by('-score')[:1]],

		} 
	},
	'ooshop':{
		'category': OoshopCategory,
		'product': OoshopProduct,
		'query':{
			'auchan':lambda p: [serialize_product(sim.auchan_product, 'auchan') for sim in ProductSimilarity.objects.filter(index_name = 'auchan', query_name = 'ooshop', ooshop_product__id = p['id'], ooshop_product__brand__brandmatch__dalliz_brand = p['dalliz_brand']).order_by('-score')[:1]],
			'monoprix':lambda p: [serialize_product(sim.monoprix_product, 'monoprix') for sim in ProductSimilarity.objects.filter(index_name = 'monoprix', query_name = 'ooshop', ooshop_product__id = p['id'], ooshop_product__brand__brandmatch__dalliz_brand = p['dalliz_brand']).order_by('-score')[:1]],
		}
	}
}

def get_subs_dalliz(id = None):
	if id:
		return DallizCategory.objects.filter(parent_category__id = id)
	else:
		return DallizCategory.objects.filter(parent_category__isnull = True)

def build_dalliz_tree(id = None):
	categories = get_subs_dalliz(id)
	response = { cat.id : {'name': cat.name, 'display': (lambda x : x.parent_category.name+' / '+x.name if x.parent_category is not None else x.name)(cat),'subs':build_dalliz_tree(cat.id)} for cat in categories}
	return response

def serialize_product(product, osm):
	return {
				'id': product.id,
				'osm': osm,
				'url':product.url,
				'image_url':product.image_url,
				'name':product.name,
				'comment': product.comment,
				'brand':(lambda x: x.brand.name if x.brand is not None else '')(product),
				'brand_db':product.brand,
				'dalliz_brand':(lambda x: x.brand.brandmatch_set.all()[0].dalliz_brand if x.brand is not None and len(x.brand.brandmatch_set.all())>0 else None)(product),
				'unit_price':(lambda x: x[0].unit_price if len(x)>0 else 0 )(product.history_set.all().order_by('-created')),
				'price': (lambda x: x[0].price if len(x)>0 else 0 )(product.history_set.all().order_by('-created')),
				'quantity': (lambda x: int(x[0].price/x[0].unit_price*1000)/1000.0 if len(x)>0 else 0 )(product.history_set.all().order_by('-created')),
				'unit':(lambda x: x.name if x is not None else 'Unknown')(product.unit),
				'possible_categories': [[{'id':x.id, 'name':x.name} for x in c.dalliz_category.all()] for c in product.categories.all()][0],
				'categories': [{'id':x.id, 'name':(lambda i: i.parent_category.name+' / '+i.name if i.parent_category is not None else i.name)(x)} for x in product.dalliz_category.all()],
				'tags': [{'name':tag.name, 'id':tag.id} for tag in product.tag.all()],
				'possible_tags':list(itertools.chain(*[[[{'id':t.id, 'name':t.name} for t in x.tags.all()] for x in c.dalliz_category.all()] for c in product.categories.all()][0]))
			}

def category(request, osm, category_id):
	# Getting dalliz category
	response = {}
	dalliz_category = DallizCategory.objects.filter(id = category_id)
	if len(dalliz_category) == 0:
		response['status'] = 404
		response['msg'] = 'Dalliz category not found'
	else:
		
		dalliz_category = dalliz_category[0]

		# Getting osm corresponding categories
		if osm not in available_osms:
			response['status'] = 404
			response['msg'] = 'Osm not available'
		else:
			Category = available_osms[osm]['category']
			osm_categories = Category.objects.filter(dalliz_category = dalliz_category)

			# Get products for each category
			response['categories'] = []
			for cat in osm_categories:
				try:
					products = [ serialize_product(p, osm) for p in cat.newproduct_set.all()  ]
				except Exception, e:
					products = [ serialize_product(p, osm) for p in cat.product_set.all()  ]

				# gettings similarities
				for p in products:
					p['similarities'] = {}
					for osm_index in available_osms:
						if osm != osm_index:
							p['matches'] = {}
							p['similarities'] = {}
							# Getting match
							match = ProductMatch.objects.all()
							if osm == 'auchan':
								match = match.filter(auchan_product = p['id'])
							if osm == 'ooshop':
								match = match.filter(ooshop_product = p['id'])
							if osm == 'monoprix':
								match = match.filter(monoprix_product = p['id'])

							if len(match) != 0:
								match = match[0]
								if osm_index == 'ooshop':
									if match.ooshop_product is not None:
										p['matches'][osm_index] = serialize_product(match.ooshop_product, osm_index)
									else:
										p['similarities'][osm_index] =  available_osms[osm]['query'][osm_index](p)
								if osm_index == 'auchan':
									if match.auchan_product is not None:
										p['matches'][osm_index] = available_osms[osm]['query'][osm_index](serialize_product(match.auchan_product, osm_index))
									else:
										p['similarities'][osm_index] =  available_osms[osm]['query'][osm_index](p)
								if osm_index == 'monoprix':
									if match.monoprix_product is not None:
										p['matches'][osm_index] = available_osms[osm]['query'][osm_index](serialize_product(match.monoprix_product, osm_index))
									else:
										p['similarities'][osm_index] =  available_osms[osm]['query'][osm_index](p)
							else:
								p['similarities'][osm_index] =  available_osms[osm]['query'][osm_index](p)

							# Filter similarities by  dalliz brand


				response['categories'].append( {
					'name' : cat.name,
					'id' : cat.id,
					'products' : products
				})
		response['category'] = {
			'name': dalliz_category.name,
			'osm': osm
		}
		# dalliz categories
		dalliz_categories = build_dalliz_tree()
		response["dalliz_categories"] = json.dumps(dalliz_categories)
		response['osm'] = osm

	# return HttpResponse(json.dumps(response))

	return render(request, 'matcher/category.html', response);

def get_match(product, osm):
	#Getting matched osms products
	if osm == 'auchan':
		match = ProductMatch.objects.filter(auchan_product = product)
	if osm == 'ooshop':
		match = ProductMatch.objects.filter(ooshop_product = product)
	if osm == 'monoprix':
		match = ProductMatch.objects.filter(monoprix_product = product)

	if len(match) ==0:
		return None
	else:
		match = match[0]

	return match


def set_categories_to_product(product, dalliz_categories, osm, set_match = True):
	"""
		Setting dalliz categories to a product
	"""
	if product is not None:
		product.dalliz_category.clear()
		[product.dalliz_category.add(c) for c in dalliz_categories]
		if set_match:
			#Getting matched osms products
			match = get_match(product, osm)
			if match:
				for other_osm in available_osms.keys():
					if other_osm != osm:
						if other_osm == 'auchan':
							set_categories_to_product(match.auchan_product, dalliz_categories, other_osm, set_match = False) 
						if other_osm == 'ooshop':
							set_categories_to_product(match.ooshop_product, dalliz_categories, other_osm, set_match = False)
						if other_osm == 'monoprix':
							set_categories_to_product(match.monoprix_product, dalliz_categories, other_osm, set_match = False)


def set_tags_to_product(product, tags, osm, set_match = True):
	"""
		Setting tags to a product
	"""
	# Clearing tags of products
	if product is not None:
		product.tag.clear()
		[product.tag.add(t) for t in tags]
		if set_match:
			#Getting matched osms products
			match = get_match(product, osm)
			if match:
				for other_osm in available_osms.keys():
					if other_osm != osm:
						if other_osm == 'auchan':
							set_tags_to_product(match.auchan_product, tags, other_osm, set_match = False) 
						if other_osm == 'ooshop':
							set_tags_to_product(match.ooshop_product, tags, other_osm, set_match = False)
						if other_osm == 'monoprix':
							set_tags_to_product(match.monoprix_product, tags, other_osm, set_match = False)

def comment(request, osm, product_id):
	"""
		Saves product comment.
	"""
	response = {}
	if request.method == 'POST':
		comment = request.POST['comment']
		if comment is not None:
			if osm in available_osms:
				Product = available_osms[osm]['product']
				product = Product.objects.filter(id = product_id)
				if len(product)==0:
					response['status'] = 404
					response['msg'] = 'Product Not found, not able to save comment'
				else:
					product = product[0]
					product.comment = comment
					product.save()
					response['status'] = 200
			else:
				response['status'] = 404
				response['msg'] = 'Osm not handled'
	
		else:
			response['status'] = 404
			response['msg'] = 'No comment was sent'
	else:
		response['status'] = 404
		response['msg'] = 'Not handling this method'

	return HttpResponse(json.dumps(response))

def tags(request, osm, product_id, tags):
	response = {}
	if osm in available_osms:
		Product = available_osms[osm]['product']
		product = Product.objects.filter(id = product_id)
		if len(product)==0:
			response['status'] = 404
			response['msg'] = 'Product Not found, not able to save tags'
		else:
			product = product[0]
			if tags != ',':
				tags = tags.split(',')
				db_tags = []
				for t in tags:
					tag, created = Tag.objects.get_or_create(name = t)
					db_tags.append(tag)
			else:
				db_tags = []
			set_tags_to_product(product, db_tags, osm, set_match = True)
			response['status'] = 200
	else:
		response['status'] = 404
		response['msg'] = 'Osm not handled'
	return HttpResponse(json.dumps(response))

def set_categories(request, osm, product_id):
	response = {}
	if request.method == 'POST':
		id_categories = request.POST.getlist('categories[]')
		if id_categories is not None:
			# Getting dalliz_categories
			categories = [ DallizCategory.objects.get(id = id_cat) for  id_cat in id_categories]
			if osm in available_osms:
				Product = available_osms[osm]['product']
				product = Product.objects.filter(id = product_id)
				if len(product)==0:
					response['status'] = 404
					response['msg'] = 'Product Not found, not able to save categories'
				else:
					product = product[0]
					# Clearing dalliz categories of products
					set_categories_to_product(product, categories, osm, set_match = True)
					response['status'] = 200
			else:
				response['status'] = 404
				response['msg'] = 'Osm not handled'
		else:
			response['status'] = 404
			response['msg'] = 'No categories were sent'
	else:
		response['status'] = 404
		response['msg'] = 'Not handling this method'
	return HttpResponse(json.dumps(response))

def autocomplete_category(request):
	"""
		Get all categories that are like term

		For instance : term = 'fr' -> resultats : 'fraise', 'africe' etc..
	"""
	term = ''
	if request.method == 'GET':
		term = unaccent(request.GET['term']).lower()
	possible_categories = DallizCategory.objects.raw( "SELECT * FROM dalliz_category WHERE LOWER(UNACCENT(name)) LIKE %s", ('%'+term+'%',))
	# Filtering possibile categories, removing categories with childs
	categories = []
	for p in possible_categories:
		if len(DallizCategory.objects.filter(parent_category = p))==0:
			categories.append(p)
	response = [{'id':t.id,'label':(lambda i: i.parent_category.name+' / '+i.name if i.parent_category is not None else i.name)(t)+' - '+str(t.id),'value':(lambda i: i.parent_category.name+' / '+i.name if i.parent_category is not None else i.name)(t)+' - '+str(t.id)} for t in categories]	
	return HttpResponse(json.dumps(response))

def set_match(request, osm, osm_from, product_id_to, product_id_from):
	response = {}
	# Getting product
	ProductFrom = available_osms[osm_from]['product']
	ProductTo = available_osms[osm]['product']
	product_from = ProductFrom.objects.get(id = product_id_from)
	product_to = ProductTo.objects.get(id = product_id_to)
	if request.method == 'POST':
		# Clearing match
		match_from = get_match(product_from, osm_from) # update this if exists
		if match_from is not None:
			if osm_from == 'auchan':
				match_from.auchan_product = None
				match_from.save()
			if osm_from == 'ooshop':
				match_from.ooshop_product = None
				match_from.save()
			if osm_from == 'monoprix':
				match_from.monoprix_product = None
				match_from.save()

		match_to = get_match(product_to, osm) # update/create this
		if match_to is None:
			if osm == 'auchan':
				match_to = ProductMatch(auchan_product = product_to)
			if osm == 'ooshop':
				match_to = ProductMatch(ooshop_product = product_to)
			if osm == 'monoprix':
				match_to = ProductMatch(monoprix_product = product_to)

		if osm_from == 'auchan':
			match_to.auchan_product = product_from
			match_to.save()
		if osm_from == 'ooshop':
			match_to.ooshop_product = product_from
			match_to.save()
		if osm_from == 'monoprix':
			match_to.monoprix_product = product_from
			match_to.save()

		# Setting same categories and tags
		dalliz_categories = product_to.dalliz_category.all()
		tags = product_to.tag.all()
		set_categories_to_product(product_from, dalliz_categories,osm_from, set_match = False)
		set_tags_to_product(product_from, tags, osm_from, set_match = False)

	if request.method == 'DELETE':
		# Clearing match
		match_to = get_match(product_to, osm) # update this
		if match_to is not None:
			if osm_from == 'auchan':
				match_to.auchan_product = None
				match_to.save()
			if osm_from == 'ooshop':
				match_to.ooshop_product = None
				match_to.save()
			if osm_from == 'monoprix':
				match_to.monoprix_product = None
				match_to.save()

	return HttpResponse(json.dumps(response))


