from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader

import simplejson as json

from osmscraper.unaccent import unaccent

from dalliz.models import Category
from tags.models import Tag

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

def set_tags_to_products(old_tags, new_tags, category):
	"""
		Sets tags for products in category.
		For every product of the category, remove tags that are not in new_tags and add new tags from new_tags.
		If a tag is in common to both lists but is not present in product tags, do not add it.

		Input:
			- new_tags : list of Tag entities
			- old_tags : list of Tag entities
			- category : Category entity
	"""
	# Compute difference between tags list
	new, common, removed = diff(old_tags, new_tags)

	products = []
	# Get all products of Category from every osm
	# Monoprix
	for cat in category.monoprix_category_dalliz_category.all():
		products = products + list(cat.newproduct_set.all())
	# Auchan
	for cat in category.auchan_category_dalliz_category.all():
		products = products + list(cat.newproduct_set.all())
	# Ooshop
	for cat in category.ooshop_category_dalliz_category.all():
		products = products + list(cat.newproduct_set.all())


	# Setting tags :
	for product in products:
		tags = product.tag.all()
		tags_to_remove = [t for t in tags if t in removed]
		tags_to_add = new
		# print new
		# print common
		# print removed
		[product.tag.remove(t) for t in tags_to_remove] # removing tag
		[product.tag.add(t) for t in tags_to_add] # removing tag

	return tags_to_add, tags_to_remove


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
		old_tags = list(category.tags.all()) # important to convert to list ohterwise it is a generator and if the tags are removed, old tags become empty
		category.tags.clear() # Removing exsisting relationships
		if tags:
			tags_string = tags.split(',')
		else:
			tags_string = []
		for tag in tags_string:
			if tag not in [' ', '', '\t', '\r', '\n']:
				tag_db, created = Tag.objects.get_or_create(name = tag)
				category.tags.add(tag_db)
		new_tags = list(category.tags.all())
		set_tags_to_products(old_tags, new_tags, category)
	if request.method == 'GET':
		tags = ','.join([ t.name for t in category.tags.all()])
		response['tags'] = tags

	return HttpResponse(json.dumps(response))

def autocomplete(request):
	"""
		Get all tags that are like term

		For instance : term = 'fr' -> resultats : 'fraise', 'africe' etc..
	"""
	term = ''
	if request.method == 'GET':
		term = unaccent(request.GET['term']).lower()
	possible_tags = Tag.objects.raw( "SELECT * FROM tags_tag WHERE LOWER(UNACCENT(name)) LIKE %s", ('%'+term+'%',))
	response = [{'id':t.id,'label':t.name,'value':t.name} for t in possible_tags]	
	return HttpResponse(json.dumps(response))

