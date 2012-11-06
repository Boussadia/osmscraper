#!/usr/bin/python
# -*- coding: utf-8 -*-

import pystache
import simplejson as json
import hashlib
from time import time

from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, redirect
from django.template import Context, loader

from templates import templates

from osmscraper.utility import *

from monoprix.models import User

def user(function):
	def wrapper(request, *args, **kwargs):
		# Getting information of called method and updating dict
		RENDER_DICT = {'meta_description': "Dalliz est un comparateur de panier entre les différents supermarchés en lignes. Avec Dalliz, gagnez du temps, économisez de l'argent.", 'user_set': False}
		# Getting informations about user
		session_key = request.session.session_key
		if session_key is None:
			request.session.set_test_cookie()
		else:
			if request.session.test_cookie_worked():
				request.session.delete_test_cookie()
				print 'Test cookie set correctly, removing it!'
				add_cart(session_key)
			else:
				if 'token' in request.session:
					print "Getting user with token : "+request.session['token']
					user, cart = get_cart_for_token(request.session['token'])
					if user is not None and cart is not None:
						print "Cart an user retrieved from datastore."
						RENDER_DICT.update({'user': user, 'user_set': True})
						RENDER_DICT.update({'cart':cart})
					else:
						print "Removing session from session"
						del request.session['token']
				else:
					print 'Retrieving cart information from datastore'
					cart = get_cart_for_session_key(session_key)
					if cart is not None:
						RENDER_DICT.update({'cart':cart})

		template_path, render_dict = function(request, *args, **kwargs)
		RENDER_DICT.update(render_dict)

		if 'token' in RENDER_DICT:
			request.session['token'] = RENDER_DICT['token']
			request.session.modified = True

		return render(request, template_path, RENDER_DICT)

	return wrapper


@user
def index(request):
	return 'dalliz/index.html', {}

@user
def a_propos(request):
	return 'dalliz/a-propos.html', {}

@user
def partenariat(request):
	return 'dalliz/partenariat.html', {}

@user
def product(request, name):
	# Fetching product from database
	product_list = get_product_from_short_url(name)
	if len(product_list) == 0:
		raise Http404
	else:
		product = product_list[0]
		product_template = templates.Product()
		product_template.set_product(product)
		product_name = product['product_name']
		brand_name = product['brand_name']
		description = 'Comparer le produit '+product_name+' de la marque '+product['brand_name']+u' dans les différents supermarchés en ligne.'
		render_dict = {'content':product_template.render(), 'meta_description': description, 'title': product_name, 'brand': brand_name}

		return 'dalliz/product.html',render_dict

@user
def category(request, sub_category):
	categories = get_same_level_categories(sub_category)
	category_names = [cat['name'] for cat in categories if cat['is_current_category']]
	if len(category_names) == 0:
		raise Http404
	else:
		category_name = category_names[0]
		products, brands = get_products_for_sub_category(sub_category)
		parent_category = get_parent_category(sub_category)
		category_template = templates.Category()
		category_template.set_products(products)
		category_template.set_brands(brands)
		category_template.set_categories(categories)
		category_template.set_parent_category(parent_category)
		
		description = u'Comparer les produits de la catégories '+category_name+u' parmis tous les supermarchés en lignes!'
		render_dict = {u'content':category_template.render(), 'meta_description': description, 'title': category_name}
		return 'dalliz/category.html', render_dict

@user
def cart(request):
	token = None
	if 'token' in request.session :
		token = request.session['token']
	elif request.session.session_key is not None:
		token = request.session.session_key

	if token is not None:
		totals = get_cart_price(token)
		cart = get_cart_for_session_key(token)
		cart_template = templates.Cart()
		cart_template.set_cart(cart)
		cart_template.set_totals(totals)

		render_dict = {u'content': cart_template.render()}
		return 'dalliz/cart.html', render_dict


def add_to_cart(request):
	if request.method == 'POST':
		product_id = request.POST['product_id']
		if 'token' in request.session and product_id is not None:
			add_product_to_cart(request.session['token'], product_id)
			return HttpResponse(json.dumps({'status':200}))
		elif request.session.session_key is not None and product_id is not None:
			add_product_to_cart(request.session.session_key, product_id)
			return HttpResponse(json.dumps({'status':200}))
		else:
			return HttpResponse(json.dumps({'status':500}))	
	else:
		return HttpResponse(json.dumps({'status':500}))

def remove_from_cart(request):
	if request.method == 'POST':
		product_id = request.POST['product_id']
		if 'token' in request.session and product_id is not None:
			remove_product_from_cart(request.session['token'], product_id)
			return HttpResponse(json.dumps({'status':200}))
		if request.session.session_key is not None and product_id is not None:
			remove_product_from_cart(request.session.session_key, product_id)
			return HttpResponse(json.dumps({'status':200}))
		else:
			return HttpResponse(json.dumps({'status':500}))	
	else:
		return HttpResponse(json.dumps({'status':500}))


@user
def cgu(request):
	return 'dalliz/cgu.html', {}

@user
def mentions(request):
	return 'dalliz/mentions.html', {}

@user
def login(request):
	login_template = templates.Login()
	render_dict = {}
	template_path = 'dalliz/login.html'

	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		users = User.objects.all().filter(email = email)
		exists = len(users) > 0
		salt = 'MaBaAb12!'
		if 'create' in request.POST:
			if exists:
				print "User already exists" 
			elif len(password)>5:
				print 'New User with email : '+email
				timestamp = time()
				hashpass = hashlib.md5(salt+password+str(time())).hexdigest()
				token = hashlib.md5(salt+email+str(time())).hexdigest()
				print token
				render_dict['token'] = token
				cart = add_cart(token)
				user = User(email=email, password = hashpass, token = token, cart=cart)
				user.save()
				render_dict['user'] = user
		elif 'connect' in request.POST:
			if exists:
				user = users[0]
				print 'Connecting '+user.email
				token = hashlib.md5(salt+email+str(time())).hexdigest()
				render_dict['token'] = token
				user.token = token
				user.cart.session_key = token
				user.cart.save()
				user.save()

	render_dict[u'content'] = login_template.render()
	return template_path, render_dict


def logout(request):
	if 'token' in request.session:
		users = User.objects.all().filter(token = request.session['token'])
		if len(users)>0:
			users[0].token = ''
			users[0].save()
	request.session.flush()
	response = redirect('/')
	# response.delete_cookie('sessionid')
	return response




