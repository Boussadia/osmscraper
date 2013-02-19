from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
from django.core import serializers

from dalliz.models import NewBrand as Brand

import simplejson as json

def index(request):
	brands = Brand.objects.filter(parent_brand__isnull=True)
	basic_json_models = json.loads(serializers.serialize("json", brands))
	models = [{'id': j['pk']} for j in basic_json_models]
	for i in xrange(0, len(models)):
		models[i].update(basic_json_models[i]['fields'])
	for i in xrange(0,len(models)):
		models[i]['url'] = str(models[i]['id'])
		models[i]['parent_id'] = None
	return render(request, 'brand_builder/index.html', {'brands': json.dumps(models)})

def sub_brands(request, id):
	response = {}
	# Getting element corresponding to url
	brand = Brand.objects.filter(id = id)
	if len(brand) == 1:
		# Found brand
		brand = brand[0]
		# Getting path to brand
		# First get ordered list of parents
		url_parents = str(brand.id)
		do = True
		current_parent = brand
		while do:
			parent =  current_parent.parent_brand

			if parent:
				url_parents = str(parent.id)+'/'+url_parents
				current_parent = parent
			else:
				do = False
		response['status'] = '200'

		if request.method == 'POST':
			response['status'] = '404'
			name = request.POST['name']

			# Verifying that model is unique
			sub_brands = Brand.objects.filter(name = name)
			if len(sub_brands) == 0:
				new_sub_brand = Brand(name = name, parent_brand = brand)
				new_sub_brand.save()

				response['status'] = '200'
				
				basic_json_model = json.loads(serializers.serialize("json", [new_sub_brand]))
				
				model = [{'id': j['pk']} for j in basic_json_model][0]
				model.update(basic_json_model[0]['fields'])

				model['url'] = url_parents+ '/'+ str(model['id'])
				model['parent_id'] = brand.id
				model['id'] = new_sub_brand.id
				response['model'] = model


		sub_brands = Brand.objects.filter(parent_brand__id__exact=id)
		basic_json_models = json.loads(serializers.serialize("json", sub_brands))
		models = [{'id': j['pk']} for j in basic_json_models]
		for i in xrange(0, len(models)):
			models[i].update(basic_json_models[i]['fields'])
		for i in xrange(0,len(models)):
			models[i]['url'] = url_parents+ '/'+ str(models[i]['id'])
			models[i]['parent_id'] = brand.id
			models[i]['id'] = sub_brands[i].id


		response['models'] = models
	elif id == 0 or id=='0':
		if request.method == 'POST':
			try:
				name = request.POST['name']
				brand = Brand(name=name)
				brand.save()
				basic_json_model = json.loads(serializers.serialize("json", [brand]))
				
				model = [{'id': j['pk']} for j in basic_json_model][0]
				model.update(basic_json_model[0]['fields'])

				model['url'] = ''
				model['parent_id'] = None
				model['id'] = brand.id
				response['status'] = '200'
				response['model'] = model
			except Exception, e:
				print e
				response['status'] = '404'
	else:
		response['status'] = '404'

	return HttpResponse(json.dumps(response))

def delete_brand(request, id):
	response = {}
	# Delete method
	if request.method == 'DELETE':
		# Getting brand
		brand = Brand.objects.filter(id = id)
		if len(brand) == 1:
			# Getting all sub brands and delete them
			id_brands_to_delete = [brand[0].id]
			cursor = 0
			while cursor<len(id_brands_to_delete):
				# Getting direct sub brands of model at position : cursor
				current_id = id_brands_to_delete[cursor]
				sub_brands_to_remove = Brand.objects.filter(parent_brand__id__exact=current_id)
				id_brands_to_delete = id_brands_to_delete + [ s.id for s in sub_brands_to_remove]
				cursor += 1

			id_brands_to_delete.reverse() # We have to delete the child before deleting the parents
			for i in xrange(0, len(id_brands_to_delete)):
				id_brand = id_brands_to_delete[i]
				Brand.objects.get(id = id_brand).delete()
			response['status'] = '200'

		else:
			response['status'] = '404'
	else:
		response['status'] = '404'

	return HttpResponse(json.dumps(response))