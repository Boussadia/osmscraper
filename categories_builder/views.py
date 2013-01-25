from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
from django.core import serializers

from dalliz.models import Category

import simplejson as json

def index(request):
	categories = Category.objects.filter(parent_category__isnull=True)
	json_categories = [j['fields'] for j in json.loads(serializers.serialize("json", categories))]
	return render(request, 'categories_builder/index.html', {'categories': json.dumps(json_categories)})

def sub_categories(request, url):
	response = {}
	# Getting element corresponding to url
	category = Category.objects.filter(url = url)
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
				url_parents = url_parents+'/'+parent.url
				current_parent = parent
			else:
				do = False
		response['status'] = '200'

		if request.method == 'GET':

			# print url_parents
			sub_categories = Category.objects.filter(parent_category__url__exact=url)
			models = [j['fields'] for j in json.loads(serializers.serialize("json", sub_categories))]
			for i in xrange(0,len(models)):
				models[i]['url'] = url_parents+ '/'+ models[i]['url']
				models[i]['parent_url'] = category.url

			response['models'] = models

		if request.method == 'POST':
			response['status'] = '404'
			name = request.POST['name']
			url = request.POST['url']

			# Verifying that model is unique
			sub_categories = Category.objects.filter(parent_category = category).filter(name = name)
			print sub_categories
			if len(sub_categories) == 0:
				new_sub_category = Category(name = name, parent_category = category, url = url)
				new_sub_category.save()
				response['status'] = '200'
				model = [j['fields'] for j in json.loads(serializers.serialize("json", [new_sub_category]))][0]
				model['url'] = url_parents+ '/'+ model['url']
				model['parent_url'] = category.url
				response['model'] = model
	else:
		response['status'] = '404'




	return HttpResponse(json.dumps(response))