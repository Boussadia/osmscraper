import simplejson as json

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
from django.core import serializers
from django.db import connection, transaction

from osmscraper.utility import dictfetchall
from osmscraper.unaccent import unaccent

from ooshop.models import Product as Ooshop_product
from ooshop.models import Product_history as Ooshop_product_history
from monoprix.models import Product as Monoprix_product
from dalliz.models import Product as Dalliz_product


def index(request):
	element_id = 'reference-'+Ooshop_product.objects.all().order_by('reference')[:1][0].reference
	return render(request, 'ooshop_monoprix/index.html', {'element_id': element_id})

def suggestions(request, id):
	result = {}
	if 'reference-' in id:
		id = id.split('reference-')[1]

	if request.method == 'GET':
		# Getting product corresponding at id
		product = Ooshop_product.objects.get(reference=id)
		product_json = json.loads(serializers.serialize("json", [product]))[0]["fields"]
		product_history = Ooshop_product_history.objects.filter(product_id = id).order_by('-timestamp')[0]
		product_json['price'] = product_history.price
		product_json['unit_price'] = product_history.unit_price

		result['product'] = product_json

		# Fetching categories of product:
		ooshop_categories = product.category.all()[0]
		categories = ooshop_categories.dalliz_category.all()
		categories_json = [ element['fields'] for element in json.loads(serializers.serialize("json", categories))]
		result['product']['categories'] = categories_json


		# Fetching related suggestions
		sql_query = ("SELECT ooshop_monoprix_matching.score as score , max(monoprix_product.id) as id, monoprix_product.title as product_name, monoprix_brand.name as brand_name , monoprix_product.url, monoprix_product.image_url,  monoprix_product.unit_price as unit_price,monoprix_product.price as price , dalliz_unit.name as unit "
					"FROM ooshop_monoprix_matching "
					"JOIN ooshop_product ON ooshop_monoprix_matching.ooshop_product_id = ooshop_product.reference "
					"JOIN monoprix_product ON monoprix_product.id = ooshop_monoprix_matching.monoprix_product_id "
					"JOIN monoprix_brand ON monoprix_brand.id = monoprix_product.brand_id "
					"JOIN monoprix_unit_dalliz_unit ON monoprix_product.unit_id = monoprix_unit_dalliz_unit.from_unit_id "
					"JOIN dalliz_unit ON dalliz_unit.id = monoprix_unit_dalliz_unit.to_unit_id "
					"WHERE ooshop_product.reference = '"+str(id)+"' "
					"GROUP BY  ooshop_monoprix_matching.score , monoprix_product.title, monoprix_brand.name , monoprix_product.url, monoprix_product.image_url, monoprix_product.unit_price, dalliz_unit.name, monoprix_product.price "
					"ORDER BY ooshop_monoprix_matching.score DESC "
					" ")
		cursor = connection.cursor()
		cursor.execute(sql_query)
		result['suggestions'] = dictfetchall(cursor)
	if request.method == 'POST':
		post = request.POST
		id_monoprix = post["id_monoprix"]
		add_matching(id, id_monoprix)
		result['status'] = 200


	return HttpResponse(json.dumps(result))

def next(request, id):
	result = {}
	if 'reference-' in id:
		id = id.split('reference-')[1]
	# id_next = int(id)+1
	products = Ooshop_product.objects.order_by('reference').filter(reference__gte=id)
	
	if len(products)>1:
		product = products[1]
		result = {'id': product.reference}
		result['status'] = 200
	else:
		result['status'] = 404
	return HttpResponse(json.dumps(result))

def previous(request, id):
	result = {}
	if 'reference-' in id:
		id = id.split('reference-')[1]
	products = Ooshop_product.objects.order_by('-reference').filter(reference__lte=id)

	if len(products)>1:
		product = products[1]
		result = {'id': product.reference}
		result['status'] = 200
	else:
		result['status'] = 404
	return HttpResponse(json.dumps(result))


def cancel(request, id):
	if 'reference-' in id:
		id = id.split('reference-')[1]
	if request.method == 'POST':
		remove_matching(id)
		result = {'status': 200}
		return HttpResponse(json.dumps(result))

def add_matching(ooshop_id, monoprix_id):
	product_ooshop = Ooshop_product.objects.get(reference=ooshop_id)
	product_monoprix = Monoprix_product.objects.get(id=monoprix_id)
	product_ooshop.monoprix_product = product_monoprix
	product_ooshop.save()

	# Creating or getting dalliz_product
	# url = "-".join("-".join(unaccent(product_telemarket.monoprix_product.title).lower().split(' ')).split("'"))
	# dalliz_products = Dalliz_product.objects.filter(url = url)
	# if len(dalliz_products)==0:
	# 	dalliz_product = Dalliz_product(url=url,brand = product_telemarket.monoprix_product.brand.dalliz_brand )
	# 	dalliz_product.save()
	# 	# Setting categories of dalliz_products
	# 	for category in product_telemarket.monoprix_product.category.all():
	# 		for dalliz_category in category.dalliz_category:
	# 			try:
	# 				dalliz_product.product_categories.add(dalliz_category)
	# 			except Exception, e:
	# 				print e
	# 		for category in product_telemarket.category.all():
	# 			for dalliz_category in category.dalliz_category:
	# 				try:
	# 					dalliz_product.product_categories.add(dalliz_category)
	# 				except Exception, e:
	# 					print e
	# else:
	# 	dalliz_product = dalliz_products[0]

	# product_telemarket.monoprix_product.dalliz_product = dalliz_product
	# product_telemarket.dalliz_product = dalliz_product

	# product_telemarket.monoprix_product.save()
	# product_telemarket.save()

def remove_matching(ooshop_id):
	product_ooshop = Ooshop_product.objects.get(reference=ooshop_id)
	# product_ooshop.monoprix_product.dalliz_product = None
	product_ooshop.monoprix_product.save()
	product_ooshop.monoprix_product = None
	# product_ooshop.dalliz_product = None
	product_ooshop.save()



