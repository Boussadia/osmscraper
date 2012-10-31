from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader

import simplejson as json

from osmscraper.utility import get_product_from_short_url

def index(request):
	return render(request, 'dalliz/index.html', {})

def a_propos(request):
	return render(request, 'dalliz/a-propos.html', {})

def partenariat(request):
	return render(request, 'dalliz/partenariat.html', {})

def product(request, name):
	# Fetching product
	result = get_product_from_short_url(name)

	return HttpResponse(json.dumps(result))