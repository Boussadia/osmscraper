#!/usr/bin/python
# -*- coding: utf-8 -*-

import pystache
import simplejson as json

from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.template import Context, loader

from templates import templates

from osmscraper.utility import get_product_from_short_url, get_products_for_sub_category

RENDER_DICT = {'meta_description': "Dalliz est un comparateur de panier entre les différents supermarchés en lignes. Avec Dalliz, gagnez du temps, économisez de l'argent."}

def index(request):
	return render(request, 'dalliz/index.html', RENDER_DICT)

def a_propos(request):
	return render(request, 'dalliz/a-propos.html', RENDER_DICT)

def partenariat(request):
	return render(request, 'dalliz/partenariat.html', RENDER_DICT)

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
		RENDER_DICT.update({'content':product_template.render(), 'meta_description': description, 'title': product_name, 'brand': brand_name})

		return render(request, 'dalliz/product.html', RENDER_DICT)

def category(request, sub_category):
	products, brands = get_products_for_sub_category(sub_category)
	print sub_category
	if len(products) == 0:
		raise Http404
	else:
		category_template = templates.Category()
		category_template.set_products(products)
		category_template.set_brands(brands)
		RENDER_DICT.update({u'content':category_template.render()})
		return render(request, 'dalliz/category.html', RENDER_DICT)
		# return HttpResponse(category_template.render())

