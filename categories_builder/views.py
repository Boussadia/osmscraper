from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
from django.core import serializers

from dalliz.models import Category

import simplejson as json

def index(request):
	categories = Category.objects.filter(parent_category__isnull=True)
	json_categories = [j['fields'] for j in json.loads(serializers.serialize("json", categories))]
	for i in xrange(0,len(json_categories)):
		json_categories[i]['id'] = categories[i].id
	return render(request, 'categories_builder/index.html', {'categories': json.dumps(json_categories)})

def sub_categories(request, parent_url = None, url = ''):
	response = {}
	# Getting element corresponding to url
	category = Category.objects.filter(url = url)
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
			sub_categories = Category.objects.filter(parent_category = category)
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
			sub_categories = Category.objects.filter(parent_category = category).filter(name = name)
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

def delete_category(request, id):
	response = {}
	# Delete method
	if request.method == 'DELETE':
		# Getting category
		category = Category.objects.filter(id = id)
		if len(category) == 1 and category[0].parent_category is not None:
			# Getting all sub categories and delete them
			id_categories_to_delete = [category[0].id]
			cursor = 0
			while cursor<len(id_categories_to_delete):
				# Getting direct sub categories of model at position : cursor
				current_id = id_categories_to_delete[cursor]
				sub_categories_to_remove = Category.objects.filter(parent_category__id__exact=current_id)
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