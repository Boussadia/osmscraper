#!/usr/bin/python
# -*- coding: utf-8 -*-

import pystache
import simplejson as json
import hashlib
from time import time
import re

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from brand_matcher.templates import templates

from ooshop.models import NewBrand as OoshopBrand
from monoprix.models import NewBrand as MonoprixBrand
from auchan.models import Brand as AuchanBrand
from dalliz.models import NewBrand as DallizBrand
from matcher.models import BrandMatch



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
	if osm == 'ooshop':
		Brand = OoshopBrand
	elif osm == 'monoprix':
		Brand = MonoprixBrand

	brand = Brand.objects.get(id= id)
	osm_brand_template_value = {
		'name': brand.name,
		'id': brand.id,
		'dalliz_brand_ids': [brandmatch.dalliz_brand.id for brandmatch in brand.brandmatch_set.all()],
		'is_set_next_id': False,
		'is_set_previous_id': False,
		'osm': osm
	}


	# Next and previous elements : 
	next_brands = Brand.objects.filter(id__gte = int(id)+1).order_by('id')
	previous = Brand.objects.filter(id__lte= int(id)-1).order_by('-id')

	if len(next_brands)>0:
		osm_brand_template_value['is_set_next_id'] = True
		osm_brand_template_value['next_id'] = next_brands[0].id
	if len(previous)>0:
		osm_brand_template_value['is_set_previous_id'] = True
		osm_brand_template_value['previous_id'] = previous[0].id

	template.set_osm_brand(osm_brand_template_value)

	matches_template_value = [ { 'id': match.dalliz_brand.id, 'name': match.dalliz_brand.name, 'score': match.score, 'is_match': (match.dalliz_brand.id in osm_brand_template_value['dalliz_brand_ids']) } for match in brand.brandsimilarity_set.filter(index_name='dalliz').distinct('dalliz_brand').order_by('-score')]

	template.set_dalliz_brands(matches_template_value)

	template_value = {
		'osm_brand': osm_brand_template_value,
		'dalliz_brands': matches_template_value
	}


	template_content = template.get_template(template.template_name)

	return request, u'brand_matcher/index.html', {u'content': template.render(), u'template': template_content, u'template_value': json.dumps(template_value)}



def cancel(request, osm, id):
	response = {}
	if request.method == 'POST':
		if osm == 'ooshop':
			Brand = OoshopBrand
		elif osm == 'monoprix':
			Brand = MonoprixBrand
		osm_brand = Brand.objects.filter(id=id)

		if len(osm_brand) == 1:
			# Found entities in database
			osm_brand = osm_brand[0]

			# Setting match
			# osm_brand.dalliz_brand = None
			# osm_brand.save()
			osm_brand.brandmatch_set.clear()

			response = {'status': 200}
		else:
			response = {'status': 404}
	else:
		response = {'status': 404}

	return HttpResponse(json.dumps(response))

def set(request, osm, osm_brand_id, dalliz_brand_id):
	response = {}
	if request.method == 'POST':
		if osm == 'ooshop':
			Brand = OoshopBrand
		elif osm == 'monoprix':
			Brand = MonoprixBrand
		osm_brand = Brand.objects.filter(id=osm_brand_id)
		dalliz_brand = DallizBrand.objects.filter(id=dalliz_brand_id)

		if len(osm_brand) == 1 and len(dalliz_brand) == 1:
			# Found entities in database
			osm_brand = osm_brand[0]
			dalliz_brand = dalliz_brand[0]

			# Setting match
			# osm_brand.dalliz_brand = dalliz_brand
			# osm_brand.save()
			match, created = BrandMatch.objects.get_or_create(dalliz_brand = dalliz_brand)
			osm_brand.brandmatch_set.clear()
			osm_brand.brandmatch_set.add(match)

			response = {'status': 200}
		else:
			response = {'status': 404}
	else:
		response = {'status': 404}

	return HttpResponse(json.dumps(response))

