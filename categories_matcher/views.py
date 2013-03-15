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


available_osms = {
	'ooshop':{
		'category':ooshop.models.Category
	},
	'auchandirect':{
		'category':auchan.models.Category
	},
	'monoprix':{
		'category':monoprix.models.Category
	}
}

def get_subs_dalliz(id = None):
	if id:
		return dalliz.models.Category.objects.filter(parent_category__id = id)
	else:
		return dalliz.models.Category.objects.filter(parent_category__isnull = True)

def buil_dalliz_tree(id = None):
	categories = get_subs_dalliz(id)
	response = { cat.id : {'name': cat.name, 'display': (lambda x : x.parent_category.name+' / '+x.name if x.parent_category is not None else x.name)(cat),'subs':buil_dalliz_tree(cat.id)} for cat in categories}
	return response

def diff(l1,l2):
	"""
		Compute difference between 2 lists. Returns new, common and removed items.
		Example : 
			l1 = [1,2,3]
			l2 = [1,3,4]
			ouput : new = [4], common = [1,3], removed = [2]

		Input :
			- l1 : a list
			- l2 : a list
		Ouput : 
			- new, common, removed : a tupple of 3 lists
	"""
	removed = [t for t in l1 if t not in l2]
	new = [t for t in l2 if t not in l1]
	common = [t for t in l1 if t in l2]
	return new, common,removed

def set_dalliz_categories_to_products(old_dalliz_categories, new_dalliz_categories, category):
	"""
		Sets dalliz_category for products in osm category.
		For every product of the category, remove dalliz categories that are not in new categories and add new categories from new dalliz categories.
		If a dalliz category is in common to both lists but is not present in product dalliz categories, do not add it.

		Input:
			- new_dalliz_categories : list of dalliz category entities
			- old_dalliz_categories : list of dalliz category entities
			- category : osm category entity
	"""
	# Compute difference between tags list
	new, common, removed = diff(old_dalliz_categories, new_dalliz_categories)

	# Get all products of Category from osm
	products = list(category.newproduct_set.all())


	# Setting tags :
	for product in products:
		dalliz_categories = product.dalliz_category.all()
		dalliz_categories_to_remove = [c for c in dalliz_categories if c in removed]
		dalliz_categories_to_add = new
		[product.dalliz_category.remove(c) for c in dalliz_categories_to_remove] # removing category
		[product.dalliz_category.add(c) for c in dalliz_categories_to_add] # adding category

	return dalliz_categories_to_add, dalliz_categories_to_remove

def migrate():
	# putting all dalliz category to corresponding products
	for category in dalliz.models.Category.objects.all():
		# Getting all products
		products = []
		for cat in category.monoprix_category_dalliz_category.all():
			products = products + list(cat.newproduct_set.all())
		# Auchan
		for cat in category.auchan_category_dalliz_category.all():
			products = products + list(cat.product_set.all())
		# Ooshop
		for cat in category.ooshop_category_dalliz_category.all():
			products = products + list(cat.newproduct_set.all())

		# Setting dalliz categories :
		[product.dalliz_category.add(category) for product in products] # adding category

def index(request):
	response = {}
	# Getting parent categories
	response = buil_dalliz_tree()

	return render(request, 'categories_matcher/index.html', {"categories": json.dumps(response)})



def categories(request, osm, level, parent='0'):
	response = {}
	Category = None

	if osm in available_osms.keys():
		Category = available_osms[osm]['category']

	if Category:
		categories = Category.objects.all()

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

		if osm in available_osms.keys():
			category_final = available_osms[osm]['category'].objects.get(id=id_category_final)

		if category_final is not None:
			old_dalliz_categories = list(category_final.dalliz_category.all())
			category_final.dalliz_category.add(category_dalliz)
			new_dalliz_categories = list(category_final.dalliz_category.all())
			set_dalliz_categories_to_products(old_dalliz_categories, new_dalliz_categories, category_final)


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

		if osm in available_osms.keys():
			category_final = available_osms[osm]['category'].objects.get(id=id_category_final)

		if category_final is not None:
			old_dalliz_categories = list(category_final.dalliz_category.all())
			category_final.dalliz_category.remove(category_dalliz)
			new_dalliz_categories = list(category_final.dalliz_category.all())
			set_dalliz_categories_to_products(old_dalliz_categories, new_dalliz_categories, category_final)

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
		response[dalliz_categories[i].id] = (lambda x : x.parent_category.name+' / '+x.name if x.parent_category is not None else x.name)(dalliz_categories[i])

	return HttpResponse(json.dumps(response))
	
