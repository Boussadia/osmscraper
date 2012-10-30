from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader

import simplejson as json

def index(request):
	return render(request, 'dalliz/index.html', {})

def a_propos(request):
	return render(request, 'dalliz/a-propos.html', {})

def partenariat(request):
	return render(request, 'dalliz/partenariat.html', {})