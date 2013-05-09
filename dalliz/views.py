#!/usr/bin/python
# -*- coding: utf-8 -*-

import pystache
import simplejson as json
import hashlib
from time import time
import re

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, redirect
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt

from templates import templates
# from osmscraper.utility import *
# from monoprix.models import User, Cart
from dalliz.models import Prospect

def user(function):
	def wrapper(request, *args, **kwargs):
		# Getting information of called method and updating dict
		RENDER_DICT = {'meta_description': "Faites des économies sur vos courses en ligne en trouvant le prix le moins cher pour votre panier !", 'user_set': False}
		template_path, render_dict = function(request, *args, **kwargs)
		RENDER_DICT.update(render_dict)

		return render(request, template_path, RENDER_DICT)

	return wrapper


def logged(function):
	def wrapper(request, *args, **kwargs):
		if 'token' in request.session:
			return user(function)(request, *args, **kwargs)
		else:
			return redirect('/login')
	return wrapper


@user
def index(request):
	return 'dalliz/landing.html', {}

@user
def a_propos(request):
	return 'dalliz/a-propos.html', {}

@user
def partenariat(request):
	return 'dalliz/partenariat.html', {}


@user
def cgu(request):
	return 'dalliz/cgu.html', {}

@user
def mentions(request):
	return 'dalliz/mentions.html', {}

@csrf_exempt
def prospects(request):
	response = {}
	if request.method == 'POST':
		regex = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
		mail = request.POST['mail']
		if re.search(regex, mail):
			prospect, created = Prospect.objects.get_or_create(mail= mail)
			nb_prospects = len(Prospect.objects.all())

			if created:
				subject = 'Master Courses, le comparateur de panier'
				message ="""Bonjour,

Bienvenue sur Master Courses !

Grâce à ce nouveau service, vous pourrez faire vos courses en ligne en toute simplicité, et avec la garantie des prix les moins chers.

Nous vous enverrons bientôt un identifiant pour pouvoir utiliser Master Courses en exclusivité !

A bientôt,

L'équipe Master Courses """
				send_mail(subject, message, 'hello@dalliz.com', [mail], fail_silently=False)
				send_mail('Nouveau prospect', 'Mail : '+mail+'.\nNombre d\'inscrits : '+str(nb_prospects), 'hello@dalliz.com', ['hello@dalliz.com'] , fail_silently=False)


			response = {'status': 200}
		else:
			response = {'status': 500}
	else:
		response = {'status': 403}

	return HttpResponse(json.dumps(response))

