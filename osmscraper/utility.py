#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import connection


def dictfetchall(cursor):
		"Generator of all rows from a cursor"
		desc = cursor.description
		return [ dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall() ]

def get_product_from_short_url(short_url):
	sql_query = ("SELECT monoprix_product.id, monoprix_product.title as product_name, monoprix_product.url, monoprix_brand.name as brand_name, LEAST(monoprix_product.price, telemarket_product.price) as price, LEAST(monoprix_product.unit_price, telemarket_product.unit_price) as unit_price, monoprix_product.unit_id, monoprix_product.image_url, monoprix_product.promotion, monoprix_product.category_id, monoprix_product.description, monoprix_product.ingredients, monoprix_product.valeur_nutritionnelle, monoprix_product.conservation, monoprix_product.conseil, monoprix_product.composition "
				"FROM monoprix_product "
				"JOIN telemarket_product ON telemarket_product.monoprix_product_id=monoprix_product.id "
				"JOIN monoprix_brand ON monoprix_product.brand_id = monoprix_brand.id "
				"WHERE dalliz_url='"+short_url+"'")
	cursor = connection.cursor()
	cursor.execute(sql_query)
	result_db = dictfetchall(cursor)
	result = []
	for i in xrange(0,len(result_db)):
		result.append({'items':[]})

		for key, val in result_db[i].iteritems():
			if key in ['description',  'ingredients', 'valeur_nutritionnelle', 'conservation', 'conseil', 'composition']:
				result[-1]['items'].append({
					'id': key,
					'name': key.replace('_',' '),
					'isNotEmpty': val is not None,
				})
				if val is not None:
					result[-1]['items'][-1]['content'] = val
			else:
				result[-1][key] = val
	return result

def get_product_from_category_id(category_id):
	sql_query = ("SELECT monoprix_product.id,  monoprix_product.dalliz_url as short_url, monoprix_product.category_id, monoprix_product.title as product_name, monoprix_product.url, monoprix_brand.name as brand_name, monoprix_brand.id as brand_id, LEAST(monoprix_product.price, telemarket_product.price) as price, LEAST(monoprix_product.unit_price, telemarket_product.unit_price) as unit_price, monoprix_product.unit_id, monoprix_product.image_url, monoprix_product.promotion, monoprix_product.category_id, monoprix_product.description, monoprix_product.ingredients, monoprix_product.valeur_nutritionnelle, monoprix_product.conservation, monoprix_product.conseil, monoprix_product.composition "
				"FROM monoprix_product "
				"JOIN telemarket_product ON telemarket_product.monoprix_product_id=monoprix_product.id "
				"JOIN monoprix_brand ON monoprix_product.brand_id = monoprix_brand.id "
				"JOIN monoprix_category_final_dalliz_category ON monoprix_category_final_dalliz_category.category_final_id =monoprix_product.category_id "
				"JOIN dalliz_category_sub ON dalliz_category_sub.id = monoprix_category_final_dalliz_category.category_sub_id "
				"WHERE dalliz_category_sub.id = "+str(category_id)+" ")
	cursor = connection.cursor()
	cursor.execute(sql_query)
	result_db = dictfetchall(cursor)
	result = []
	for i in xrange(0,len(result_db)):
		result.append({'items':[]})

		for key, val in result_db[i].iteritems():
			if key in ['description',  'ingredients', 'valeur_nutritionnelle', 'conservation', 'conseil', 'composition']:
				result[-1]['items'].append({
					'id': key,
					'name': key.replace('_',' '),
					'isNotEmpty': val is not None,
				})
				if val is not None:
					result[-1]['items'][-1]['content'] = val
			else:
				result[-1][key] = val
	return result

def get_products_for_sub_category(sub_category_url):
	sql_query_categories = ("SELECT id, name, url as short_url FROM dalliz_category_sub "
							"WHERE dalliz_category_sub.url = '"+sub_category_url+"' ")
	cursor = connection.cursor()
	cursor.execute(sql_query_categories)
	category_db = dictfetchall(cursor)
	if len(category_db)==0:
		return [], []
	else:
		category_id = category_db[0]['id']
		result = get_product_from_category_id(category_id)
		products = result
		brands_temp = {}
		for i in xrange(0,len(result)):
			brands_temp[result[i]['brand_id']] = result[i]['brand_name']

		brands = []
		for id, name in brands_temp.iteritems():
			brands.append({"id":id, "name": name})
	return products, brands

def get_same_level_categories(sub_category_url):
	sql_query_categories = ("SELECT  (t.id = dalliz_category_sub.id ) as is_current_category ,dalliz_category_sub.id, name, url as short_url FROM dalliz_category_sub "
							"JOIN (SELECT parent_category_id, id FROM dalliz_category_sub WHERE url = '"+sub_category_url+"') AS t ON t.parent_category_id = dalliz_category_sub.parent_category_id")
	cursor = connection.cursor()
	cursor.execute(sql_query_categories)
	category_db = dictfetchall(cursor)
	return category_db