#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import connection
from monoprix.models import Cart, Product, User, Cart_content


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
				"WHERE telemarket_product.monoprix_product_id is not null and dalliz_category_sub.id = "+str(category_id)+" "
				"ORDER BY monoprix_brand.name")
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
		brands = []
		for i in xrange(0,len(result)):
			if len(brands)==0:
				brands.append({"id":result[i]['brand_id'], "name": result[i]['brand_name']})
			elif brands[-1]["id"] != result[i]['brand_id']:
				brands.append({"id":result[i]['brand_id'], "name": result[i]['brand_name']})
	return products, brands

def get_same_level_categories(sub_category_url):
	sql_query_categories = ("SELECT  (t.id = dalliz_category_sub.id ) as is_current_category ,dalliz_category_sub.id, name, url as short_url FROM dalliz_category_sub "
							"JOIN (SELECT parent_category_id, id FROM dalliz_category_sub WHERE url = '"+sub_category_url+"') AS t ON t.parent_category_id = dalliz_category_sub.parent_category_id "
							"ORDER BY position")
	cursor = connection.cursor()
	cursor.execute(sql_query_categories)
	category_db = dictfetchall(cursor)
	return category_db

def get_parent_category(sub_category_url):
	sql = "SELECT parent_category_id FROM dalliz_category_sub WHERE url='"+sub_category_url+"';";
	cursor = connection.cursor()
	cursor.execute(sql)
	parent_category_db = dictfetchall(cursor)
	if len(parent_category_db)>0:
		parent_category_id = parent_category_db[0]['parent_category_id']
		if parent_category_id == 1:
			return 'entretien'
		elif parent_category_id == 2:
			return 'alimentaire'
		else:
			return 'hygiene'
	else:
		return None



def get_cart_for_session_key(session_key):
	carts = Cart.objects.all().filter(session_key=session_key)
	if len(carts)>0:
		return get_cart(carts[0])
	else:
		return None

def get_cart_for_token(token):
	users = User.objects.all().filter(token=token)
	if len(users)>0:
		user_db = users[0]
		cart = user_db.cart
		result = get_cart(cart)
		user = {'name':user_db.first_name, 'first_name':user_db.first_name ,'last_name':user_db.last_name, 'email': user_db.email, 'sex': user_db.sex  }
		if user['name'] == "":
			user['name'] = user['email'].split('@')[0]
		return user, result
	else:
		return None, None

def get_cart(cart):
	product_in_carts = Cart_content.objects.filter(cart=cart)
	if len(product_in_carts)>0:
		products_db = [ {'product':p_in_c.product, 'quantity':p_in_c.quantity} for p_in_c in product_in_carts]
		result = {}
		result['quantity'] = sum( [p['quantity'] for p in products_db] )
		result['products'] = []
		for i in xrange(0, len(products_db)):
			for j in xrange(0,products_db[i]['quantity']):
				result['products'].append({'dalliz_url': products_db[i]['product'].dalliz_url, 'image_url': products_db[i]['product'].image_url, 'id': products_db[i]['product'].id, 'title': products_db[i]['product'].title, 'brand_name':products_db[i]['product'].brand.name})
		return result
	else:
		return None

def get_cart_price(session_key):
	sql_telemarket = ("SELECT telemarket_product.price as price, monoprix_cart_content.quantity as quantity, monoprix_product.id "
					"FROM monoprix_cart_content "
					"JOIN monoprix_product ON monoprix_cart_content.product_id = monoprix_product.id "
					"JOIN telemarket_product ON telemarket_product.monoprix_product_id = monoprix_product.id "
					"JOIN monoprix_cart ON monoprix_cart.id = monoprix_cart_content.cart_id "
					"WHERE monoprix_cart.session_key = '"+session_key+"';")

	sql_monoprix = ("SELECT monoprix_product.price AS price ,monoprix_cart_content.quantity AS quantity,monoprix_product.id "
					"FROM monoprix_cart_content "
					"JOIN monoprix_product ON monoprix_cart_content.product_id = monoprix_product.id "
					"JOIN monoprix_cart ON monoprix_cart.id = monoprix_cart_content.cart_id "
					"WHERE monoprix_cart.session_key = '"+session_key+"';")

	cursor = connection.cursor()
	cursor.execute(sql_telemarket)
	telemarket_db = dictfetchall(cursor)
	telemarket = {'name':'Telemaket','class':'telemarket', 'price': sum( (product['price']*product['quantity'] for product in telemarket_db) )}
	telemarket['livraison'] = get_livraison_telemarket(telemarket['price'])
	telemarket['total'] = telemarket['livraison'] + telemarket['price']

	cursor = connection.cursor()
	cursor.execute(sql_monoprix)
	monoprix_db = dictfetchall(cursor)
	monoprix = {'name':'Monoprix','class':'monoprix', 'price': sum( (product['price']*product['quantity'] for product in monoprix_db) )}
	monoprix['livraison'] = get_livraison_monoprix(monoprix['price'])
	monoprix['total'] = monoprix['livraison'] + monoprix['price']

	if telemarket['total'] > monoprix['total']:
		monoprix['is_min'] = True
		monoprix['percent'] = monoprix['total']/telemarket['total']*100
		telemarket['percent'] = 100.0
		monoprix['difference'] = telemarket['total'] - monoprix['total']
		if monoprix['price']>= 70:
			monoprix['thereshold_ok'] = True
		else:
			monoprix['thereshold_not_ok'] = True
			monoprix['thereshold'] = 70-monoprix['price']
	else:
		telemarket['is_min'] = True
		telemarket['percent'] = telemarket['total']/monoprix['total']*100
		monoprix['percent'] = 100.0
		telemarket['difference'] = monoprix['total'] - telemarket['total']
		if telemarket['price']>=40:
			telemarket["thereshold_ok"] = True
		else:
			telemarket['thereshold_not_ok'] = True
			telemarket["thereshold"] = 40-telemarket['price']


	return monoprix, telemarket

def get_livraison_monoprix(amount):
	price = 0.0
	if amount<149:
		price = 9
	elif amount<189:
		price = 5
	return price

def get_livraison_telemarket(amount):
	price = 0.0
	if amount<80:
		price = 14.90
	elif amount<150:
		price = 9.90
	elif amount<180:
		price = 5.90
	elif amount<190:
		price = 2.90
	return price

def add_cart(session_key):
	cart = Cart(session_key =session_key)
	cart.save()
	return cart

def add_product_to_cart(session_key, product_id):
	print 'In add  cart. session_key : '+session_key+' and product_id = '+str(product_id)
	products = Product.objects.filter(id=product_id)
	if len(products)==0:
		return
	else:
		product = products[0]

	carts = Cart.objects.filter(session_key = session_key)

	if len(carts) == 0:
		cart = add_cart(session_key)
	else:
		cart = carts[0]

	product_in_carts = Cart_content.objects.filter(cart=cart, product = product)

	if len(product_in_carts)>0:
		product_in_cart = product_in_carts[0]
	else:
		product_in_cart = Cart_content(cart=cart, product = product)

	try:
		product_in_cart.quantity = product_in_cart.quantity + 1
		product_in_cart.save()
	except Exception, e:
		print 'Something went wrong in add cart. session_key : '+session_key+' and product_id = '+str(product_id)

def remove_product_from_cart(session_key, product_id):
	products = Product.objects.filter(id=product_id)
	if len(products)==0:
		return
	else:
		product = products[0]

	carts = Cart.objects.filter(session_key = session_key)

	if len(carts) == 0:
		cart = add_cart(session_key)
	else:
		cart = carts[0]

	product_in_carts = Cart_content.objects.filter(cart=cart, product = product)

	if len(product_in_carts)>0:
		product_in_cart = product_in_carts[0]
		if product_in_cart.quantity>1:
			product_in_cart.quantity = product_in_cart.quantity - 1
			product_in_cart.save()
		elif product_in_cart.quantity<=1:
			product_in_cart.delete()