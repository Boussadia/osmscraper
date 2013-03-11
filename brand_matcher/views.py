#!/usr/bin/python
# -*- coding: utf-8 -*-

import pystache
import simplejson as json
import hashlib
from time import time
import re

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from ooshop_brand_matcher.templates import templates

from ooshop.models import *
from dalliz.models import Brand as Dalliz_brand



def hijax(function):
	def wrapper(*args, **kwargs):
		request, django_template_path , dict_template = function(*args, **kwargs)
		if request.is_ajax():
			# This is an ajax call, do not render template with django, return mustache template and associated values
			response = {
				'template': dict_template['template'],
				'template_value': dict_template['template_value']
			}
			return HttpResponse(json.dumps(response))
		else:
			# This is not an ajax call, return rendered django template
			return render(request, django_template_path, dict_template);

	return wrapper

@hijax
def selector(request, osm, id):
	template = templates.Brand_selector()
	brand = Brand.objects.get(id= id)
	ooshop_brand_template_value = {
		'name': brand.name,
		'id': brand.id,
		'dalliz_brand_ids': [dalliz_brand.id for dalliz_brand in brand.dalliz_brand_m2m.all()],
		'is_set_next_id': False,
		'is_set_previous_id': False
	}

	# Next and previous elements : 
	next_brands = Brand.objects.filter(id__gte = int(id)+1).order_by('id')
	previous = Brand.objects.filter(id__lte= int(id)-1).order_by('-id')

	if len(next_brands)>0:
		ooshop_brand_template_value['is_set_next_id'] = True
		ooshop_brand_template_value['next_id'] = next_brands[0].id
	if len(previous)>0:
		ooshop_brand_template_value['is_set_previous_id'] = True
		ooshop_brand_template_value['previous_id'] = previous[0].id

	template.set_ooshop_brand(ooshop_brand_template_value)

	matches_template_value = [ { 'id': match.dalliz_brand.id, 'name': match.dalliz_brand.name, 'score': match.score, 'is_match': (match.dalliz_brand.id in ooshop_brand_template_value['dalliz_brand_ids']) } for match in Brand_matching.objects.filter(ooshop_brand = brand).order_by('-score')]
	template.set_dalliz_brands(matches_template_value)

	template_value = {
		'ooshop_brand': ooshop_brand_template_value,
		'dalliz_brands': matches_template_value
	}


	template_content = template.get_template(template.template_name)

	return request, u'ooshop_brand_matcher/index.html', {u'content': template.render(), u'template': template_content, u'template_value': json.dumps(template_value)}



def cancel(request, osm, id):
	response = {}
	if request.method == 'POST':
		ooshop_brand = Brand.objects.filter(id=id)

		if len(ooshop_brand) == 1:
			# Found entities in database
			ooshop_brand = ooshop_brand[0]

			# Setting match
			# ooshop_brand.dalliz_brand = None
			# ooshop_brand.save()
			ooshop_brand.dalliz_brand_m2m.clear()

			response = {'status': 200}
		else:
			response = {'status': 404}
	else:
		response = {'status': 404}

	return HttpResponse(json.dumps(response))

def set(request, osm, osm_brand_id, dalliz_brand_id):
	response = {}
	if request.method == 'POST':
		ooshop_brand = Brand.objects.filter(id=osm_brand_id)
		dalliz_brand = Dalliz_brand.objects.filter(id=dalliz_brand_id)

		if len(ooshop_brand) == 1 and len(dalliz_brand) == 1:
			# Found entities in database
			ooshop_brand = ooshop_brand[0]
			dalliz_brand = dalliz_brand[0]

			# Setting match
			# ooshop_brand.dalliz_brand = dalliz_brand
			# ooshop_brand.save()
			ooshop_brand.dalliz_brand_m2m.add(dalliz_brand)

			response = {'status': 200}
		else:
			response = {'status': 404}
	else:
		response = {'status': 404}

	return HttpResponse(json.dumps(response))

