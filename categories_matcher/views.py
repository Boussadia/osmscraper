from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader

import simplejson as json

import telemarket
import place_du_marche
import monoprix
import coursengo
import dalliz

def index(request):
	categories = {}
	sub_categories = dalliz.models.Category_sub.objects.all()
	for i in xrange(0,len(sub_categories)):
		categories[sub_categories[i].id] = sub_categories[i].name
	return render_to_response('categories_matcher/index.html', {"categories": categories})

def categories(request, osm, level, parent="1"):
	response = {"final":False}

	# Telemarket get response
	if osm == "telemarket":
		if level == "1":
			main_categories = telemarket.models.Category_main.objects.all()
			for i in xrange(0, len(main_categories)):
				response[main_categories[i].id] = main_categories[i].name
		elif level == "2":
			sub_categories = telemarket.models.Category_sub_1.objects.all().filter(parent_category_id=parent)
			for i in xrange(0, len(sub_categories)):
				response[sub_categories[i].id] = sub_categories[i].name
		elif level == "3":
			sub_categories = telemarket.models.Category_sub_2.objects.all().filter(parent_category_id=parent)
			for i in xrange(0, len(sub_categories)):
				response[sub_categories[i].id] = sub_categories[i].name
		elif level == "4":
			sub_categories = telemarket.models.Category_sub_3.objects.all().filter(parent_category_id=parent)
			for i in xrange(0, len(sub_categories)):
				response[sub_categories[i].id] = sub_categories[i].name
		elif level == "5":
			sub_categories = telemarket.models.Category_final.objects.all().filter(parent_category_id=parent)
			for i in xrange(0, len(sub_categories)):
				response[sub_categories[i].id] = sub_categories[i].name
			response["final"] = True

	# Monoprix get response
	if osm == "monoprix":
		if level == "1":
			main_categories = monoprix.models.Category_main.objects.all()
			for i in xrange(0, len(main_categories)):
				response[main_categories[i].id] = main_categories[i].name
		elif level == "2":
			sub_categories = monoprix.models.Category_sub_level_1.objects.all().filter(parent_category_id=parent)
			for i in xrange(0, len(sub_categories)):
				response[sub_categories[i].id] = sub_categories[i].name
		elif level == "3":
			sub_categories = monoprix.models.Category_sub_level_2.objects.all().filter(parent_category_id=parent)
			for i in xrange(0, len(sub_categories)):
				response[sub_categories[i].id] = sub_categories[i].name
		elif level == "4":
			sub_categories = monoprix.models.Category_final.objects.all().filter(parent_category_id=parent)
			for i in xrange(0, len(sub_categories)):
				response[sub_categories[i].id] = sub_categories[i].name
			response["final"] = True

	# Place du marche get response
	if osm == "place_du_marche":
		if level == "1":
			main_categories = place_du_marche.models.Category_main.objects.all()
			for i in xrange(0, len(main_categories)):
				response[main_categories[i].id] = main_categories[i].name
		elif level == "2":
			sub_categories = place_du_marche.models.Category_sub.objects.all().filter(parent_category_id=parent)
			for i in xrange(0, len(sub_categories)):
				response[sub_categories[i].id] = sub_categories[i].name
		elif level == "3":
			sub_categories = place_du_marche.models.Category_final.objects.all().filter(parent_category_id=parent)
			for i in xrange(0, len(sub_categories)):
				response[sub_categories[i].id] = sub_categories[i].name
			response["final"] = True

	# Coursengo get response
	if osm == "coursengo":
		if level == "1":
			main_categories = coursengo.models.Category_main.objects.all()
			for i in xrange(0, len(main_categories)):
				response[main_categories[i].id] = main_categories[i].name
		elif level == "2":
			sub_categories = coursengo.models.Category_sub_level_1.objects.all().filter(parent_category_id=parent)
			for i in xrange(0, len(sub_categories)):
				response[sub_categories[i].id] = sub_categories[i].name
		elif level == "3":
			sub_categories = coursengo.models.Category_final.objects.all().filter(parent_category_id=parent)
			for i in xrange(0, len(sub_categories)):
				response[sub_categories[i].id] = sub_categories[i].name
			response["final"] = True
	return HttpResponse(json.dumps(response))


def add_link(request):
	if request.method == 'POST':
		post = request.POST
		osm = post["osm"]
		id_category_final = post["id_category_final"]
		id_dalliz_category = post["id_dalliz_category"]

		category_dalliz = dalliz.models.Category_sub.objects.get(id=id_dalliz_category)
		category_final = None

		if osm == "telemarket":
			category_final = telemarket.models.Category_final.objects.get(id=id_category_final)
		elif osm == "coursengo":
			category_final = coursengo.models.Category_final.objects.get(id=id_category_final)
		elif osm == "place_du_marche":
			category_final = place_du_marche.models.Category_final.objects.get(id=id_category_final)
		elif osm == "monoprix":
			category_final = monoprix.models.Category_final.objects.get(id=id_category_final)

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

		category_dalliz = dalliz.models.Category_sub.objects.get(id=id_dalliz_category)
		category_final = None

		if osm == "telemarket":
			category_final = telemarket.models.Category_final.objects.get(id=id_category_final)
		elif osm == "coursengo":
			category_final = coursengo.models.Category_final.objects.get(id=id_category_final)
		elif osm == "place_du_marche":
			category_final = place_du_marche.models.Category_final.objects.get(id=id_category_final)
		elif osm == "monoprix":
			category_final = monoprix.models.Category_final.objects.get(id=id_category_final)

		if category_final is not None:
			category_final.dalliz_category.remove(category_dalliz)

			return HttpResponse(json.dumps({"status":200}))
		else:
			return HttpResponse(json.dumps({"status":404}))

		return HttpResponse(json.dumps())

def get_links(request, osm, category_id):
	if osm == "telemarket":
		dalliz_categories = dalliz.models.Category_sub.objects.filter(telemarket_category_final_category_dalliz=category_id)
	elif osm == "coursengo":
		dalliz_categories = dalliz.models.Category_sub.objects.filter(coursengo_category_final_category_dalliz=category_id)
	elif osm == "place_du_marche":
		dalliz_categories = dalliz.models.Category_sub.objects.filter(place_du_marche_category_final_category_dalliz=category_id)
	elif osm == "monoprix":
		dalliz_categories = dalliz.models.Category_sub.objects.filter(monoprix_category_final_category_dalliz=category_id)

	response = {}

	for i in xrange(0, len(dalliz_categories)):
		response[dalliz_categories[i].id] = dalliz_categories[i].name

	return HttpResponse(json.dumps(response))
	
