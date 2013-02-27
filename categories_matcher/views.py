from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader

import simplejson as json

import telemarket
import place_du_marche
import monoprix
import coursengo
import dalliz
import ooshop
import auchan

def index(request):
	categories = {}
	categories = dalliz.models.Category.objects.all()
	# Keeping only category leaves, i.e. category that are not parent of another category
	# if a parent category is in categories_entities, remove it but get its children
	i = 0
	categories = list(categories)
	while i<len(categories):
		category = categories[i]
		sub_categories = dalliz.models.Category.objects.filter(parent_category = category)
		if len(sub_categories) == 0:
			# This category is a leaf keep going
			i = i+1
			continue
		else:
			# This is not a leaf, remove it and add sub categories to end of list
			categories.pop(i)
			categories = categories + filter(lambda sub_cat:sub_cat not in categories, list(sub_categories))
			continue

	return render(request, 'categories_matcher/index.html', {"categories": { cat.id : cat.name for cat in categories}})

def categories(request, osm, level, parent='0'):
	response = {}
	Category = None

	if osm == "monoprix":
		Category = monoprix.models.Category
	
	if osm == "ooshop":
		Category = ooshop.models.Category

	if osm == "auchandirect":
		Category = auchan.models.Category

	if Category:
		categories = Category.objects.all()
		print parent == '0'
		if parent != '0':
			categories = categories.filter(parent_category_id = parent)
		else:
			categories = categories.filter(parent_category__isnull = True)
		

		# Are they final categories?
		for cat in categories:
			j = {'name': cat.name}
			sub_categories = Category.objects.filter(parent_category = cat)
			if sub_categories.count() == 0:
				j['final'] = True
			else:
				j['final'] = False
			response.update({cat.id: j})


	return HttpResponse(json.dumps(response))


def add_link(request):
	if request.method == 'POST':
		post = request.POST
		osm = post["osm"]
		id_category_final = post["id_category_final"]
		id_dalliz_category = post["id_dalliz_category"]

		category_dalliz = dalliz.models.Category.objects.get(id=id_dalliz_category)
		category_final = None

		if osm == "auchandirect":
			category_final = auchan.models.Category.objects.get(id=id_category_final)
		elif osm == "monoprix":
			category_final = monoprix.models.Category.objects.get(id=id_category_final)
		elif osm == "ooshop":
			category_final = ooshop.models.Category.objects.get(id=id_category_final)

		if category_final is not None:
			category_final.dalliz_category.add(category_dalliz)

			return HttpResponse(json.dumps({"status":200}))
		else:
			return HttpResponse(json.dumps({"status":404}))

def delete_link(request):
	if request.method == 'POST':
		post = request.POST
		osm = post["osm"]
		id_category_final = post["id_category_final"]
		id_dalliz_category = post["id_dalliz_category"]

		category_dalliz = dalliz.models.Category.objects.get(id=id_dalliz_category)
		category_final = None

		if osm == "auchandirect":
			category_final = auchan.models.Category.objects.get(id=id_category_final)
		elif osm == "monoprix":
			category_final = monoprix.models.Category.objects.get(id=id_category_final)
		elif osm == "ooshop":
			category_final = ooshop.models.Category.objects.get(id=id_category_final)

		if category_final is not None:
			category_final.dalliz_category.remove(category_dalliz)

			return HttpResponse(json.dumps({"status":200}))
		else:
			return HttpResponse(json.dumps({"status":404}))

		return HttpResponse(json.dumps())

def get_links(request, osm, category_id):
	if osm == "auchandirect":
		dalliz_categories = dalliz.models.Category.objects.filter(auchan_category_dalliz_category=category_id)
	elif osm == "monoprix":
		dalliz_categories = dalliz.models.Category.objects.filter(monoprix_category_dalliz_category=category_id)
	elif osm == "ooshop":
		dalliz_categories = dalliz.models.Category.objects.filter(ooshop_category_dalliz_category=category_id)

	response = {}

	for i in xrange(0, len(dalliz_categories)):
		response[dalliz_categories[i].id] = dalliz_categories[i].name

	return HttpResponse(json.dumps(response))
	
