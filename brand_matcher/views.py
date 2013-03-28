#!/usr/bin/python
# -*- coding: utf-8 -*-

import pystache
import simplejson as json
import hashlib
from time import time
import re
import itertools

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from osmscraper.unaccent import unaccent

from brand_matcher.templates import templates

from ooshop.models import Brand as OoshopBrand
from monoprix.models import Brand as MonoprixBrand
from auchan.models import Brand as AuchanBrand
from dalliz.models import Brand as DallizBrand
from matcher.models import BrandMatch

available_osm = {
	'ooshop':OoshopBrand,
	'monoprix': MonoprixBrand,
	'auchan': AuchanBrand
}



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
	if osm in available_osm:
		Brand = available_osm[osm]

	brand = Brand.objects.get(id= id)
	osm_brand_template_value = {
		'name': brand.name,
		'id': brand.id,
		'dalliz_brand_ids': [brandmatch.dalliz_brand.id for brandmatch in brand.brandmatch_set.all()],
		'dalliz_brand_names': {brandmatch.dalliz_brand.id:brandmatch.dalliz_brand.name for brandmatch in brand.brandmatch_set.all()},
		'is_set_next_id': False,
		'is_set_previous_id': False,
		'osm': osm
	}

	if osm == 'ooshop':
		# Next and previous elements : 
		next_brands = Brand.objects.filter(id__gte = int(id)+1).order_by('id')
		previous = Brand.objects.filter(id__lte= int(id)-1).order_by('-id')
		for i in xrange(0, len(next_brands)):
			if len(next_brands[i].product_set.exclude(exists = False))>0:
				osm_brand_template_value['is_set_next_id'] = True
				osm_brand_template_value['next_id'] = next_brands[i].id
				break
		for i in xrange(0, len(previous)):
			if len(previous[i].product_set.exclude(exists = False))>0:
				osm_brand_template_value['is_set_previous_id'] = True
				osm_brand_template_value['previous_id'] = previous[i].id
				break
	else:
		# Next and previous elements : 
		next_brands = Brand.objects.filter(parent_brand__isnull = True, id__gte = int(id)+1).order_by('id')
		previous = Brand.objects.filter(parent_brand__isnull = True, id__lte= int(id)-1).order_by('-id')
		if len(next_brands)>0:
			osm_brand_template_value['is_set_next_id'] = True
			osm_brand_template_value['next_id'] = next_brands[0].id
		if len(previous)>0:
			osm_brand_template_value['is_set_previous_id'] = True
			osm_brand_template_value['previous_id'] = previous[0].id

	template.set_osm_brand(osm_brand_template_value)

	matches_template_value = [ { 'id': match.dalliz_brand.id, 'name': (lambda x : x.parent_brand.name+' / '+x.name if x.parent_brand is not None else x.name)(match.dalliz_brand), 'score': match.score, 'is_match': (match.dalliz_brand.id in osm_brand_template_value['dalliz_brand_ids']) } for match in brand.brandsimilarity_set.filter(index_name='dalliz').distinct('dalliz_brand', 'score').order_by('-score')]
	[matches_template_value.append( item ) for item in [ {'id': dalliz_brand_id, 'name': osm_brand_template_value['dalliz_brand_names'][dalliz_brand_id], 'is_match': True } for dalliz_brand_id in  osm_brand_template_value['dalliz_brand_ids'] if dalliz_brand_id not in [m['id'] for m in matches_template_value]]]

	template.set_dalliz_brands(matches_template_value)

	# Adding parent brand to name if exits for dalliz brands
	# [ m.update({'name':m.dalliz_brand.parent_brand.name+'/'+m['name']}) for m in matches_template_value if m.dalliz_brand.parent_brand is not None]

	template_value = {
		'osm_brand': osm_brand_template_value,
		'dalliz_brands': matches_template_value
	}


	template_content = template.get_template(template.template_name)

	return request, u'brand_matcher/index.html', {u'content': template.render(), u'template': template_content, u'template_value': json.dumps(template_value)}



def cancel(request, osm, id):
	response = {}
	if request.method == 'POST':
		if osm in available_osm:
			Brand = available_osm[osm]
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
		if osm in available_osm:
			Brand = available_osm[osm]
		osm_brand = Brand.objects.filter(id=osm_brand_id)
		dalliz_brand = DallizBrand.objects.filter(id=dalliz_brand_id)

		if len(osm_brand) == 1 and len(dalliz_brand) == 1:
			# Found entities in database
			osm_brand = osm_brand[0]
			dalliz_brand = dalliz_brand[0]

			if osm == 'ooshop':
				match, created = BrandMatch.objects.get_or_create(ooshop_brand = osm_brand, defaults = {'dalliz_brand': dalliz_brand})
			elif osm == 'monoprix':
				match, created = BrandMatch.objects.get_or_create(monoprix_brand = osm_brand, defaults = {'dalliz_brand': dalliz_brand})
			elif osm == 'auchan':
				match, created = BrandMatch.objects.get_or_create(auchan_brand = osm_brand, defaults = {'dalliz_brand': dalliz_brand})

			match.dalliz_brand = dalliz_brand
			match.save()
			# osm_brand.brandmatch_set.clear()
			osm_brand.brandmatch_set.add(match)

			response = {'status': 200}
		else:
			response = {'status': 404}
	else:
		response = {'status': 404}

	return HttpResponse(json.dumps(response))

def autocomplete(request):
	response = {}
	term = ''
	if request.method == 'GET':
		term = unaccent(request.GET['term']).lower()
	possible_brands = DallizBrand.objects.raw( "SELECT * FROM dalliz_brand WHERE LOWER(UNACCENT(name)) LIKE %s", ('%'+term+'%',))
	response = [{'id':b.id,'label':b.name,'value':b.name, 'name':b.name} for b in possible_brands]
	return HttpResponse(json.dumps(response))

