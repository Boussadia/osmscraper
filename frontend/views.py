from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def index(request):
	return render(request, 'frontend/index.html', {})