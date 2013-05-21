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
from django.db import connection, transaction
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from tags.models import Tag

from matcher.base.stemmer import Stemmer

from ooshop.models import Category as OoshopCategory
from monoprix.models import Category as MonoprixCategory
from auchan.models import Category as AuchanCategory
from dalliz.models import Category as DallizCategory
from ooshop.models import Product as OoshopProduct
from monoprix.models import Product as MonoprixProduct
from auchan.models import Product as AuchanProduct
from matcher.models import ProductSimilarity, NoProductSimilarity
from matcher.models import ProductMatch



available_osms = {
	'auchan':{
		'category': AuchanCategory,
		'product': AuchanProduct,
		'query':{
			'ooshop':lambda p: [serialize_product(sim.ooshop_product, 'ooshop') for sim in ProductSimilarity.objects.filter(index_name = 'ooshop', query_name = 'auchan', auchan_product__id = p['id'], ooshop_product__dalliz_category__parent_category__parent_category__in = p['parent_categories'] , ooshop_product__brand__brandmatch__dalliz_brand__in = p['parent_brands'], ooshop_product__productmatch__auchan_product__isnull = True).exclude(ooshop_product__noproductsimilarity__auchan_product__id = p['id']).order_by('-score')[:1]],
			'monoprix':lambda p: [serialize_product(sim.monoprix_product, 'monoprix') for sim in ProductSimilarity.objects.filter(index_name = 'monoprix', query_name = 'auchan', auchan_product__id = p['id'], monoprix_product__dalliz_category__parent_category__parent_category__in = p['parent_categories'] , monoprix_product__brand__brandmatch__dalliz_brand__in = p['parent_brands'], monoprix_product__productmatch__auchan_product__isnull = True).exclude(monoprix_product__noproductsimilarity__auchan_product__id = p['id']).order_by('-score')[:1]],
		}
	},
	'monoprix':{
		'category': MonoprixCategory,
		'product': MonoprixProduct,
		'query':{
			'auchan':lambda p: [serialize_product(sim.auchan_product, 'auchan') for sim in ProductSimilarity.objects.filter(index_name = 'auchan', query_name = 'monoprix', monoprix_product__id = p['id'], auchan_product__dalliz_category__parent_category__parent_category__in = p['parent_categories'] , auchan_product__brand__brandmatch__dalliz_brand__in = p['parent_brands'], auchan_product__productmatch__monoprix_product__isnull = True).exclude(auchan_product__noproductsimilarity__monoprix_product__id = p['id']).order_by('-score')[:1]],
			'ooshop':lambda p: [serialize_product(sim.ooshop_product, 'ooshop') for sim in ProductSimilarity.objects.filter(index_name = 'ooshop', query_name = 'monoprix', monoprix_product__id = p['id'],  ooshop_product__dalliz_category__parent_category__parent_category__in = p['parent_categories'] , ooshop_product__brand__brandmatch__dalliz_brand__in = p['parent_brands'], ooshop_product__productmatch__monoprix_product__isnull = True).exclude(ooshop_product__noproductsimilarity__monoprix_product__id = p['id']).order_by('-score')[:1]],

		} 
	},
	'ooshop':{
		'category': OoshopCategory,
		'product': OoshopProduct,
		'query':{
			'auchan':lambda p: [serialize_product(sim.auchan_product, 'auchan') for sim in ProductSimilarity.objects.filter(index_name = 'auchan', query_name = 'ooshop', ooshop_product__id = p['id'],  auchan_product__dalliz_category__parent_category__parent_category__in = p['parent_categories'] , auchan_product__brand__brandmatch__dalliz_brand__in = p['parent_brands'], auchan_product__productmatch__ooshop_product__isnull = True).exclude(auchan_product__noproductsimilarity__ooshop_product__id = p['id']).order_by('-score')[:1]],
			'monoprix':lambda p: [serialize_product(sim.monoprix_product, 'monoprix') for sim in ProductSimilarity.objects.filter(index_name = 'monoprix', query_name = 'ooshop', ooshop_product__id = p['id'],  monoprix_product__dalliz_category__parent_category__parent_category__in = p['parent_categories'] , monoprix_product__brand__brandmatch__dalliz_brand__in = p['parent_brands'], monoprix_product__productmatch__ooshop_product__isnull = True).exclude(monoprix_product__noproductsimilarity__ooshop_product__id = p['id']).order_by('-score')[:1]],
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

def get_main_categories(categories = []):
	parent_categories = []
	for c in categories:
		if c.parent_category is None:
			parent_categories.append(c)
		else:
			parent_category = c.parent_category
			parent_categories = parent_categories + get_main_categories([parent_category])
	return list(set(parent_categories))

def get_main_brands(brands = []):
	parent_brands = []
	for b in brands:
		if b.parent_brand is None:
			parent_brands.append(b)
		else:
			parent_brand = b.parent_brand
			parent_brands = parent_brands + get_main_brands([parent_brand])
	return list(set(parent_brands))

def serialize_product(product, osm, categories = None):
	p = {
				'id': product.id,
				'osm': osm,
				'url':product.url,
				'image_url':product.image_url,
				'name':product.name,
				'comment': product.comment,
				'brand':(lambda x: x.brand.name if x.brand is not None else '')(product),
				'brand_id':(lambda x: x.brand.id if x.brand is not None else '')(product),
				'brand_db':product.brand,
				'dalliz_brand':(lambda x: x.brand.brandmatch_set.all()[0].dalliz_brand if x.brand is not None and len(x.brand.brandmatch_set.all())>0 else None)(product),
				'parent_brands': (lambda p : get_main_brands([b.dalliz_brand for b in p.brand.brandmatch_set.all()]) if p.brand is not None else [])(product),
				'unit_price':(lambda x: x[0].unit_price if len(x)>0 else 0 )(product.history_set.all().order_by('-created')),
				'price': (lambda x: x[0].price if len(x)>0 else 0 )(product.history_set.all().order_by('-created')),
				'quantity': (lambda x: int(x[0].price/x[0].unit_price*1000)/1000.0 if len(x)>0 and x[0].unit_price is not None else 0 )(product.history_set.all().order_by('-created')),
				'unit':(lambda x: x.name if x is not None else 'Unknown')(product.unit),
				# 'possible_categories': (lambda p:[[{'id':x.id, 'name':x.name} for x in c.dalliz_category.all()] for c in p.categories.all()][0] if len(p.categories.all())>0 else [])(product),
				'categories': [{'id':x.id, 'name':(lambda i: i.parent_category.name+' / '+i.name if i.parent_category is not None else i.name)(x)} for x in product.dalliz_category.all()],
				'tags': [{'name':tag.name, 'id':tag.id} for tag in product.tag.all()],
				# 'possible_tags':(lambda p:list(itertools.chain(*[[[{'id':t.id, 'name':t.name} for t in x.tags.all()] for x in c.dalliz_category.all()] for c in p.categories.all()][0] if len(p.categories.all())>0 else [])(product) ))
				'is_in_category': False,
				'parent_categories': get_main_categories(product.dalliz_category.all())
			}
	if categories:
		p['is_in_category'] = False
		for c in categories:
			if (c.id in (x['id'] for x in p['categories'])):
				p['is_in_category'] = True
				break
			else:
				continue
	return p

def category(request, osm, category_id):
	# Getting dalliz category
	response = {}
	dalliz_category = DallizCategory.objects.filter(id = category_id)
	if len(dalliz_category)>0:
		dalliz_category = dalliz_category[0]
		dalliz_categories = DallizCategory.objects.filter(parent_category = dalliz_category)
		if len(dalliz_categories) == 0:
			response['status'] = 404
			response['msg'] = 'Dalliz category not found'
		else:
			# for dalliz_category in dalliz_categories:
			# Getting osm corresponding categories
			if osm not in available_osms:
				response['status'] = 404
				response['msg'] = 'Osm not available'
			else:
				Category = available_osms[osm]['category']
				try:
					osm_categories = Category.objects.filter(dalliz_category__in = dalliz_categories, exists = True, product__id__isnull = False).distinct()
				except Exception, e:
					osm_categories = Category.objects.filter(dalliz_category__in = dalliz_categories, exists = True, product__id__isnull = False).distinct()

				# Get products for each category
				response['categories'] = []
				for cat in osm_categories:
					products = [ serialize_product(p, osm, dalliz_categories) for p in cat.product_set.filter(exists = True)  ]

					# gettings similarities
					for p in products:
						p['matches'] = {}
						p['similarities'] = {}
						for osm_index in available_osms:
							if osm != osm_index:
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
											p['matches'][osm_index] = serialize_product(match.auchan_product, osm_index)
										else:
											p['similarities'][osm_index] =  available_osms[osm]['query'][osm_index](p)
									if osm_index == 'monoprix':
										if match.monoprix_product is not None:
											p['matches'][osm_index] = serialize_product(match.monoprix_product, osm_index)
										else:
											p['similarities'][osm_index] =  available_osms[osm]['query'][osm_index](p)
								else:
									p['similarities'][osm_index] =  available_osms[osm]['query'][osm_index](p)



					response['categories'].append( {
						'name' : cat.name,
						'id' : cat.id,
						'products' : products
					})
			response['category'] = {
				'name': (lambda c: c.parent_category.name+'/'+c.name if c.parent_category is not None else c.name)(dalliz_category),
				'osm': osm,
			}
			# dalliz categories
			dalliz_categories = build_dalliz_tree()
			response["dalliz_categories"] = json.dumps(dalliz_categories)
			response['osm'] = osm
			# response['main_category'] = (lambda c: c.parent_category.parent_category.id if c.parent_category.parent_category is not None else (c.parent_category.id if c.parent_category is not None else c.id))(dalliz_category)
			response['main_category'] = (lambda c: c.parent_category.id if c.parent_category is not None else c.id)(dalliz_category)
			response['parent_category'] = dalliz_category.id
			# response['sub_category'] = dalliz_category.id
			response['osms'] = available_osms.keys()

		# return HttpResponse(json.dumps(response))

	return render(request, 'matcher/category.html', response)

def get_match(product, osm):
	#Getting matched osms products
	kwargs = {
		osm+'_product': product
	}
	match = ProductMatch.objects.filter(**kwargs)

	if len(match) ==0:
		return None
	else:
		match = match[0]

	return match

def diff(l1,l2):
	"""
		Compute difference between 2 lists. Returns new, common and removed items.
		Example : 
			l1 = [1,2,3]
			l2 = [1,3,4]
			ouput : new = [4], common = [1,3], removed = [2]

		Input :
			- l1 : a list
			- l2 : a list
		Ouput : 
			- new, common, removed : a tupple of 3 lists
	"""
	removed = [t for t in l1 if t not in l2]
	new = [t for t in l2 if t not in l1]
	common = [t for t in l1 if t in l2]
	return new, common,removed

def set_categories_to_product(product, dalliz_categories, osm, set_match = True):
	"""
		Setting dalliz categories to a product
	"""
	if product is not None:
		old_categories = product.dalliz_category.all()
		new, common, removed = diff(old_categories, dalliz_categories)
		for c in new:
			try:
				product.dalliz_category.add(c)
			except Exception, e:
				connection._rollback()
		for c in removed:
			try:
				product.dalliz_category.remove(c)
			except Exception, e:
				connection._rollback()

		if set_match:
			#Getting matched osms products
			match = get_match(product, osm)
			if match:
				[ set_categories_to_product(getattr(match,other_osm+'_product'), dalliz_categories, other_osm, set_match = False)  for other_osm in available_osms.keys() if other_osm != osm]


def set_tags_to_product(product, tags, osm, set_match = True):
	"""
		Setting tags to a product
	"""
	# Clearing tags of products
	if product is not None:
		old_tags = product.tag.all()

		new, common, removed = diff(old_tags, tags)
		for t in new:
			try:
				product.tag.add(t)
			except Exception, e:
				connection._rollback()
		for t in removed:
			try:
				product.tag.remove(t)
			except Exception, e:
				connection._rollback()

		if set_match and match is not None:
			[ set_tags_to_product(getattr(match,other_osm+'_product'), tags, other_osm, set_match = False)  for other_osm in available_osms.keys() if other_osm != osm]
@csrf_exempt
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
@csrf_exempt
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
					stemmed_name = Stemmer(t).stem_text()
					tag_db, created = Tag.objects.get_or_create(name = t, defaults =  {'stemmed_name': stemmed_name})
					if created:
						tag_db.stemmed_name = stemmed_name
						tag_db.save()
					db_tags.append(t)
			else:
				db_tags = []
			set_tags_to_product(product, db_tags, osm, set_match = True)
			response['status'] = 200
	else:
		response['status'] = 404
		response['msg'] = 'Osm not handled'
	return HttpResponse(json.dumps(response))
@csrf_exempt
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
@csrf_exempt
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
@csrf_exempt
def set_no_similarity(request, osm, osm_from, product_id_to, product_id_from):
	response = {}
	if request.method == 'POST':
		nosim = list(NoProductSimilarity.objects.raw("SELECT * FROM matcher_noproductsimilarity WHERE "+osm+"_product_id = %s and "+osm_from+"_product_id = %s", (product_id_to, product_id_from)))
		if len(nosim):
			# Relation of no similarity already exists, do not do anything
			response['status'] = 200
			response['msg'] = 'Done'
		else:
			# The similarity does not exist, create it
			# sql_insert =  # INSERT QUERY
			cursor = connection.cursor()
			cursor.execute("INSERT INTO matcher_noproductsimilarity ("+osm+"_product_id, "+osm_from+"_product_id) VALUES ( %s ,  %s )", [product_id_to, product_id_from])
			transaction.commit_unless_managed()
			response['status'] = 200
			response['msg'] = 'Added to database'

	elif request.method == 'DELETE':
		nosim = list(NoProductSimilarity.objects.raw("SELECT * FROM matcher_noproductsimilarity WHERE "+osm+"_product_id = %s and "+osm_from+"_product_id = %s", (product_id_to, product_id_from)))
		if len(nosim)>0:
			nosim = nosim[0]
			nosim.delete()
			response['status'] = 200
			response['msg'] = 'Deleted'
		else:
			response['status'] = 200
			response['msg'] = 'Nothing to do'
	else:
		response['status'] = 403
		response['msg'] = 'Method not handled'

	return HttpResponse(json.dumps(response))

@csrf_exempt
def set_match(request, osm, osm_from, product_id_to, product_id_from):
	response = {}
	# Getting product
	ProductFrom = available_osms[osm_from]['product']
	ProductTo = available_osms[osm]['product']
	product_from = ProductFrom.objects.get(id = product_id_from)
	product_to = ProductTo.objects.get(id = product_id_to)
	if request.method == 'POST':
		product_to.save()
		product_from.save()
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
		response['tags'] = [{'name':tag.name, 'id':tag.id} for tag in tags]
		response['categories'] = [{'id':x.id, 'name':(lambda i: i.parent_category.name+' / '+i.name if i.parent_category is not None else i.name)(x)} for x in dalliz_categories]
		set_categories_to_product(product_from, dalliz_categories,osm_from, set_match = False)
		set_tags_to_product(product_from, tags, osm_from, set_match = False)

	if request.method == 'DELETE':
		# Clearing match
		match_to = get_match(product_to, osm) # update this
		product = None
		if match_to is not None:
			if osm_from == 'auchan':
				product = match_to.auchan_product
				match_to.auchan_product = None
				match_to.save()
			if osm_from == 'ooshop':
				product = match_to.ooshop_product
				match_to.ooshop_product = None
				match_to.save()
			if osm_from == 'monoprix':
				product = match_to.monoprix_product
				match_to.monoprix_product = None
				match_to.save()
		if product:
			tags, categories = reset_product(product)
			response['tags'] = tags
			response['categories'] = categories


	return HttpResponse(json.dumps(response))

def reset_product(product):
	product.dalliz_category.clear()
	product.tag.clear()
	[ [ [product.dalliz_category.add(d), [ product.tag.add(t) for t in d.tags.all()]] for d in c.dalliz_category.all()] for c in product.categories.all()]
	categories = [{'id':x.id, 'name':(lambda i: i.parent_category.name+' / '+i.name if i.parent_category is not None else i.name)(x)} for x in product.dalliz_category.all()]
	tags = [{'name':tag.name, 'id':tag.id} for tag in product.tag.all()]
	return tags, categories



