import simplejson as json

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
from django.core import serializers
from django.db import connection, transaction

from telemarket.models import Product as Telemarket_product
from monoprix.models import Product as Monoprix_product

def dictfetchall(cursor):
		"Generator of all rows from a cursor"
		desc = cursor.description
		return [ dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall() ]


def index(request):
	element_id = Telemarket_product.objects.all().order_by('id')[:1][0].id
	return render(request, 'telemarket_monoprix/index.html', {'element_id': element_id})

def suggestions(request, id):
	result = {}
	if request.method == 'GET':
		# Getting product corresponding at id
		product = Telemarket_product.objects.get(id=id)
		product_json = json.loads(serializers.serialize("json", [product]))[0]["fields"]
		result['product'] = product_json

		# Fetching categories of product:
		categories = product.category.dalliz_category.all()
		categories_json = [ element['fields'] for element in json.loads(serializers.serialize("json", categories))]
		result['product']['categories'] = categories_json


		# Fetching related suggestions
		sql_query = ("SELECT telemarket_monoprix_matching.score as score , max(monoprix_product.id) as id, monoprix_product.title as product_name, monoprix_brand.name as brand_name , monoprix_product.url, monoprix_product.image_url,  monoprix_product.unit_price as unit_price,monoprix_product.price as price , dalliz_unit.name as unit "
					"FROM telemarket_monoprix_matching "
					"JOIN telemarket_product ON telemarket_monoprix_matching.telemarket_product_id = telemarket_product.id "
					"JOIN monoprix_product ON monoprix_product.id = telemarket_monoprix_matching.monoprix_product_id "
					"JOIN monoprix_brand ON monoprix_brand.id = monoprix_product.brand_id "
					"JOIN monoprix_unit_dalliz_unit ON monoprix_product.unit_id = monoprix_unit_dalliz_unit.from_unit_id "
					"JOIN dalliz_unit ON dalliz_unit.id = monoprix_unit_dalliz_unit.to_unit_id "
					"WHERE telemarket_product.id = "+str(id)+" "
					"GROUP BY  telemarket_monoprix_matching.score , monoprix_product.title, monoprix_brand.name , monoprix_product.url, monoprix_product.image_url, monoprix_product.unit_price, dalliz_unit.name, monoprix_product.price "
					"ORDER BY telemarket_monoprix_matching.score DESC "
					" ")
		cursor = connection.cursor()
		cursor.execute(sql_query)
		result['suggestions'] = dictfetchall(cursor)
	if request.method == 'POST':
		post = request.POST
		id_monoprix = post["id_monoprix"]
		product_telemarket = Telemarket_product.objects.get(id=id)
		product_monoprix = Monoprix_product.objects.get(id=id_monoprix)
		product_telemarket.monoprix_product = product_monoprix
		product_telemarket.save()
		result['status'] = 200


	return HttpResponse(json.dumps(result))

def next(request, id):
	result = {}
	id_next = int(id)+1
	products = Telemarket_product.objects.order_by('id').filter(id__gte=id_next)[:1]
	
	if len(products)>0:
		product = products[0]
		result = {'id': product.id}
		result['status'] = 200
	else:
		result['status'] = 404
	return HttpResponse(json.dumps(result))

def previous(request, id):
	result = {}
	id_previous = int(id)-1
	products = Telemarket_product.objects.order_by('-id').filter(id__lte=id_previous)[:1]
	
	if len(products)>0:
		product = products[0]
		result = {'id': product.id}
		result['status'] = 200
	else:
		result['status'] = 404
	return HttpResponse(json.dumps(result))


def cancel(request, id):
	if request.method == 'POST':
		product_telemarket = Telemarket_product.objects.get(id=id)
		product_telemarket.monoprix_product = None
		product_telemarket.save()
		result = {'status': 200}
		return HttpResponse(json.dumps(result))

