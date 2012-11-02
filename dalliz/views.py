#!/usr/bin/python
# -*- coding: utf-8 -*-

import pystache
import simplejson as json

from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.template import Context, loader

from templates import templates

from osmscraper.utility import get_product_from_short_url, get_products_for_sub_category, get_same_level_categories, get_cart_for_session_key, add_cart, add_product_to_cart

RENDER_DICT = {'meta_description': "Dalliz est un comparateur de panier entre les différents supermarchés en lignes. Avec Dalliz, gagnez du temps, économisez de l'argent."}

def user(function):
	def wrapper(request, *args, **kwargs):
		# Getting information of called method and updating dict
		template_path, render_dict = function(request, *args, **kwargs)
		RENDER_DICT.update(render_dict)

		# Getting informations about user
		session_key = request.session.session_key
		if session_key is None:
			request.session.set_test_cookie()
		else:
			if request.session.test_cookie_worked():
				request.session.delete_test_cookie()
				print 'Test cookie set correctly, removing it!'
				add_cart(session_key)
			else:
				print 'Retrieving cart information from datastore'
				cart = get_cart_for_session_key(session_key)
				print cart
				RENDER_DICT.update({'cart':cart})
		return render(request, template_path, RENDER_DICT)
	return wrapper


@user
def index(request):
	return 'dalliz/index.html', {}

@user
def a_propos(request):
	return 'dalliz/a-propos.html', {}

@user
def partenariat(request):
	return 'dalliz/partenariat.html', {}

@user
def product(request, name):
	# Fetching product from database
	product_list = get_product_from_short_url(name)
	if len(product_list) == 0:
		raise Http404
	else:
		product = product_list[0]
		product_template = templates.Product()
		product_template.set_product(product)
		product_name = product['product_name']
		brand_name = product['brand_name']
		description = 'Comparer le produit '+product_name+' de la marque '+product['brand_name']+u' dans les différents supermarchés en ligne.'
		render_dict = {'content':product_template.render(), 'meta_description': description, 'title': product_name, 'brand': brand_name}

		return 'dalliz/product.html',render_dict

@user
def category(request, sub_category):
	categories = get_same_level_categories(sub_category)
	category_names = [cat['name'] for cat in categories if cat['is_current_category']]
	if len(category_names) == 0:
		raise Http404
	else:
		category_name = category_names[0]
		products, brands = get_products_for_sub_category(sub_category)
		category_template = templates.Category()
		category_template.set_products(products)
		category_template.set_brands(brands)
		category_template.set_categories(categories)
		
		description = u'Comparer les produits de la catégories '+category_name+u' parmis tous les supermarchés en lignes!'
		render_dict = {u'content':category_template.render(), 'meta_description': description, 'title': category_name}
		return 'dalliz/category.html', render_dict

def add_to_cart(request):
	if request.method == 'POST':
		product_id = request.POST['product_id']
		if request.session.session_key is not None:
			add_product_to_cart(request.session.session_key, product_id)
		return HttpResponse(json.dumps({'status':200}))
