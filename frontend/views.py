from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings


def index(request):
	return render(request, 'frontend/index.html', {'DEBUG': settings.DEBUG})