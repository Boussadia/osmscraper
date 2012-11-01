#!/usr/bin/python
# -*- coding: utf-8 -*-

import pystache
import simplejson as json

from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.template import Context, loader

from templates import templates

from osmscraper.utility import get_product_from_short_url

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

		RENDER_DICT.update({u'content':product_template.render()})

		return render(request, 'dalliz/product.html', RENDER_DICT)