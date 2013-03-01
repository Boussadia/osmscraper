from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader

import simplejson as json

from dalliz.models import Category
from tags.models import Tag

def get_subs_dalliz(id = None):
	if id:
		return Category.objects.filter(parent_category__id = id)
	else:
		return Category.objects.filter(parent_category__isnull = True)

def buil_dalliz_tree(id = None):
	categories = get_subs_dalliz(id)
	response = { cat.id : {'name': cat.name, 'subs':buil_dalliz_tree(cat.id)} for cat in categories}
	return response

def index(request):
	response = {}
	# Getting parent categories
	categories = buil_dalliz_tree()
	tags = [ t.name for t in Tag.objects.all()]

	return render(request, 'tags/index.html', {"categories": json.dumps(categories), "tags": json.dumps(tags)})

def tags(request, id_category, tags =''):
	response = {}
	category = Category.objects.filter(id=id_category)
	if len(category) == 1:
		category = category[0]
		response['status'] = 200
	else:
		return HttpResponse(json.dumps({"status":404}))

	if request.method == 'POST':
		category.tags.clear() # Removing exsisting relationships
		if tags:
			tags_string = tags.split(';')
		else:
			tags_string = []
		for tag in tags_string:
			if tag not in [' ', '', '\t', '\r', '\n']:
				tag_db, created = Tag.objects.get_or_create(name = tag)
				category.tags.add(tag_db)
	if request.method == 'GET':
		tags = ';'.join([ t.name for t in category.tags.all()])
		response['tags'] = tags

	return HttpResponse(json.dumps(response))

