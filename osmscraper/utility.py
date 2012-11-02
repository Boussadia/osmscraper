#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import connection


def dictfetchall(cursor):
		"Generator of all rows from a cursor"
		desc = cursor.description
		return [ dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall() ]

def get_product_from_short_url(short_url):
	if settings.DEBUG:
		sql_query = (" SELECT result.id, result.title as product_name, result.url, monoprix_brand.name as brand_name, LEAST(result.price, telemarket_product.price) as price, LEAST(result.unit_price, telemarket_product.unit_price) as unit_price, result.unit_id, result.image_url, result.promotion, result.category_id, result.description, result.ingredients, result.valeur_nutritionnelle, result.conservation, result.conseil, result.composition "
					"FROM (SELECT monoprix_product.id, STRING_AGG(chunck.chuncks, '-') as short_url, title, url, brand_id, price, unit_price, unit_id, image_url, promotion, category_id, description, ingredients, valeur_nutritionnelle, conservation, conseil, composition "
					"FROM (SELECT regexp_split_to_table(unaccent(lower(title)), '(\W)+') as chuncks, id  FROM monoprix_product) as chunck "
					"JOIN monoprix_product ON chunck.id = monoprix_product.id "
					"GROUP BY monoprix_product.id) AS result "
					"JOIN monoprix_brand ON result.brand_id = monoprix_brand.id "
					"JOIN telemarket_product ON result.id = telemarket_product.monoprix_product_id "
					"WHERE short_url = '"+short_url+"' ")
	else:
		sql_query = (" SELECT result.id, result.title as product_name, result.url, monoprix_brand.name as brand_name, LEAST(result.price, telemarket_product.price) as price, LEAST(result.unit_price, telemarket_product.unit_price) as unit_price, result.unit_id, result.image_url, result.promotion, result.category_id, result.description, result.ingredients, result.valeur_nutritionnelle, result.conservation, result.conseil, result.composition "
					"FROM (SELECT monoprix_product.id, STRING_AGG(chunck.chuncks, '-') as short_url, title, url, brand_id, price, unit_price, unit_id, image_url, promotion, category_id, description, ingredients, valeur_nutritionnelle, conservation, conseil, composition "
					"FROM (SELECT regexp_split_to_table(unaccent(lower(title)), E'(\\W)+') as chuncks, id  FROM monoprix_product) as chunck "
					"JOIN monoprix_product ON chunck.id = monoprix_product.id "
					"GROUP BY monoprix_product.id) AS result "
					"JOIN monoprix_brand ON result.brand_id = monoprix_brand.id "
					"JOIN telemarket_product ON result.id = telemarket_product.monoprix_product_id "
					"WHERE short_url = '"+short_url+"' ")
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
	if settings.DEBUG:
		sql_query = (" SELECT result.id, result.short_url, result.category_id, result.title as product_name, result.url, dalliz_brand.name as brand_name,dalliz_brand.id as brand_id, LEAST(result.price, telemarket_product.price) as price, LEAST(result.unit_price, telemarket_product.unit_price) as unit_price, result.unit_id, result.image_url, result.promotion, result.category_id, result.description, result.ingredients, result.valeur_nutritionnelle, result.conservation, result.conseil, result.composition "
					"FROM (SELECT monoprix_product.id, STRING_AGG(chunck.chuncks, '-') as short_url, title, url, brand_id, price, unit_price, unit_id, image_url, promotion, category_id, description, ingredients, valeur_nutritionnelle, conservation, conseil, composition "
					"FROM (SELECT regexp_split_to_table(unaccent(lower(title)), '(\W)+') as chuncks, id  FROM monoprix_product) as chunck "
					"JOIN monoprix_product ON chunck.id = monoprix_product.id "
					"GROUP BY monoprix_product.id) AS result "
					"JOIN monoprix_brand ON result.brand_id = monoprix_brand.id "
					"JOIN telemarket_product ON result.id = telemarket_product.monoprix_product_id "
					"JOIN monoprix_category_final_dalliz_category on monoprix_category_final_dalliz_category.category_final_id =result.category_id "
					"JOIN dalliz_category_sub ON dalliz_category_sub.id = monoprix_category_final_dalliz_category.category_sub_id "
					"JOIN dalliz_brand ON dalliz_brand.id = monoprix_brand.dalliz_brand_id "
					"WHERE dalliz_category_sub.id = '"+str(category_id)+"' ")
	else:
		sql_query = (" SELECT result.id, result.short_url, result.category_id, result.title as product_name, result.url, dalliz_brand.name as brand_name,dalliz_brand.id as brand_id, LEAST(result.price, telemarket_product.price) as price, LEAST(result.unit_price, telemarket_product.unit_price) as unit_price, result.unit_id, result.image_url, result.promotion, result.category_id, result.description, result.ingredients, result.valeur_nutritionnelle, result.conservation, result.conseil, result.composition "
					"FROM (SELECT monoprix_product.id, STRING_AGG(chunck.chuncks, '-') as short_url, title, url, brand_id, price, unit_price, unit_id, image_url, promotion, category_id, description, ingredients, valeur_nutritionnelle, conservation, conseil, composition "
					"FROM (SELECT regexp_split_to_table(unaccent(lower(title)), E'(\\W)+') as chuncks, id  FROM monoprix_product) as chunck "
					"JOIN monoprix_product ON chunck.id = monoprix_product.id "
					"GROUP BY monoprix_product.id) AS result "
					"JOIN monoprix_brand ON result.brand_id = monoprix_brand.id "
					"JOIN telemarket_product ON result.id = telemarket_product.monoprix_product_id "
					"JOIN monoprix_category_final_dalliz_category on monoprix_category_final_dalliz_category.category_final_id =result.category_id "
					"JOIN dalliz_category_sub ON dalliz_category_sub.id = monoprix_category_final_dalliz_category.category_sub_id "
					"JOIN dalliz_brand ON dalliz_brand.id = monoprix_brand.dalliz_brand_id "
					"WHERE dalliz_category_sub.id = '"+str(category_id)+"' ")
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
#
# select id, STRING_AGG(chunck.chuncks, '-') as short_url from ( SELECT regexp_split_to_table(unaccent(lower(name)), '(\W)+') as chuncks, id  FROM dalliz_category_sub) as chunck group by chunck.id
# select * from (select id, STRING_AGG(chunck.chuncks, '-') as category_short_url from ( SELECT regexp_split_to_table(unaccent(lower(name)), '(\W)+') as chuncks, id  FROM dalliz_category_sub) as chunck group by chunck.id) as dalliz_cat join monoprix_category_final_dalliz_category on monoprix_category_final_dalliz_category.category_sub_id = dalliz_cat.id join monoprix_product on monoprix_product.category_id = monoprix_category_final_dalliz_category.category_sub_id
# where category_short_url= 'vaisselle'
#
# SELECT result.id as product_id, result.short_url as short_url,result.title as product_name, result.url, monoprix_brand.name as brand_name, LEAST(result.price, telemarket_product.price) as price, result.image_url, result.promotion, result.category_id FROM (SELECT monoprix_product.id, STRING_AGG(chunck.chuncks, '-') as short_url, title, url, brand_id, price, unit_price, unit_id, image_url, promotion, category_id, description, ingredients, valeur_nutritionnelle, conservation, conseil, composition FROM (SELECT regexp_split_to_table(unaccent(lower(title)), '(\W)+') as chuncks, id  FROM monoprix_product) as chunck JOIN monoprix_product ON chunck.id = monoprix_product.id GROUP BY monoprix_product.id) AS result JOIN monoprix_brand ON result.brand_id = monoprix_brand.id JOIN telemarket_product ON result.id = telemarket_product.monoprix_product_id
#

def get_products_for_sub_category(sub_category_url):
	if settings.DEBUG:
		sql_query_categories = ("SELECT * FROM "
								"(SELECT id, STRING_AGG(chunck.chuncks, '-') as short_url "
								"FROM ( SELECT regexp_split_to_table(unaccent(lower(name)), '(\W)+') as chuncks, id  FROM dalliz_category_sub) as chunck "
								"GROUP BY chunck.id ) AS result "
								"WHERE result.short_url = '"+sub_category_url+"' ")
	else:
		sql_query_categories = ("SELECT * FROM "
								"(SELECT id, STRING_AGG(chunck.chuncks, '-') as short_url "
								"FROM ( SELECT regexp_split_to_table(unaccent(lower(name)), E'(\\W)+') as chuncks, id  FROM dalliz_category_sub) as chunck "
								"GROUP BY chunck.id ) AS result "
								"WHERE result.short_url = '"+sub_category_url+"' ")
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