#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import simplejson as json

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from osmscraper.unaccent import unaccent

from dalliz.models import Category


def index(request):
	categories = Category.objects.filter(parent_category__isnull=True).order_by('position')
	json_categories = [j['fields'] for j in json.loads(serializers.serialize("json", categories))]
	for i in xrange(0,len(json_categories)):
		json_categories[i]['id'] = categories[i].id
	return render(request, 'categories_builder/index.html', {'categories': json.dumps(json_categories)})
@csrf_exempt
def sub_categories(request, parent_url = None, url = ''):
	response = {}
    # Getting element corresponding to url
	category = Category.objects.filter(url = url).order_by('position')
	if parent_url is not None:
		category = category.filter(parent_category__url = parent_url)
	else:
		category = category.filter(parent_category__isnull = True)
	if len(category) == 1:
		# Found category
		category = category[0]
		# Getting path to category
		# First get ordered list of parents
		url_parents = category.url
		do = True
		current_parent = category
		while do:
			parent =  current_parent.parent_category

			if parent:
				url_parents = parent.url+'/'+url_parents
				current_parent = parent
			else:
				do = False
		response['status'] = '200'

		if request.method == 'GET':

			# print url_parents
			sub_categories = Category.objects.filter(parent_category = category).order_by('position')
			models = [j['fields'] for j in json.loads(serializers.serialize("json", sub_categories))]
			for i in xrange(0,len(models)):
				models[i]['url'] = url_parents+ '/'+ models[i]['url']
				models[i]['parent_url'] = category.url
				models[i]['id'] = sub_categories[i].id


			response['models'] = models

		if request.method == 'POST':
			response['status'] = '404'
			name = request.POST['name']
			url = request.POST['url']

			# Verifying that model is unique
			sub_categories = Category.objects.filter(parent_category = category).filter(name = name).order_by('position')
			if len(sub_categories) == 0:
				new_sub_category = Category(name = name, parent_category = category, url = url)
				new_sub_category.save()
				response['status'] = '200'
				model = [j['fields'] for j in json.loads(serializers.serialize("json", [new_sub_category]))][0]
				model['url'] = url_parents+ '/'+ model['url']
				model['parent_url'] = category.url
				model['id'] = new_sub_category.id
				response['model'] = model
				print model
	else:
		response['status'] = '404'

	return HttpResponse(json.dumps(response))
@csrf_exempt
def change_position(request, id, position):
	response = {'status': 404}

	if request.method == 'POST':
		category = Category.objects.filter(id = id)
		if len(category) == 1:
			category = category[0]
			category.position = position
			category.save()
			response = {'status': 200}
	return HttpResponse(json.dumps(response))
@csrf_exempt
def change_name(request, id):
	response = {'status': 404}

	if request.method == 'POST':
		new_name = request.POST['name']
		category = Category.objects.filter(id = id)
		if len(category) == 1:
			category = category[0]
			category.name = new_name
			# Now working on url
			url = unaccent(new_name.lower())
			reg = r'[^a-z0-9]'
			url = '-'.join([x for x in re.split(reg, url) if x != ''])
			category.url = url
			category.save()
			response = {'status': 200, 'url': url}

	return HttpResponse(json.dumps(response))



@csrf_exempt
def delete_category(request, id):
	response = {}
	# Delete method
	if request.method == 'DELETE':
		# Getting category
		category = Category.objects.filter(id = id)
		if len(category) == 1:
			# Getting all sub categories and delete them
			id_categories_to_delete = [category[0].id]
			cursor = 0
			while cursor<len(id_categories_to_delete):
				# Getting direct sub categories of model at position : cursor
				current_id = id_categories_to_delete[cursor]
				sub_categories_to_remove = Category.objects.filter(parent_category__id__exact=current_id).order_by('position')
				id_categories_to_delete = id_categories_to_delete + [ s.id for s in sub_categories_to_remove]
				cursor += 1

			id_categories_to_delete.reverse() # We have to delete the child before deleting the parents
			for i in xrange(0, len(id_categories_to_delete)):
				id_category = id_categories_to_delete[i]
				Category.objects.get(id = id_category).delete()
			response['status'] = '200'

		else:
			response['status'] = '404'
	else:
		response['status'] = '404'

	return HttpResponse(json.dumps(response))
