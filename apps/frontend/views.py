from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings

from django.contrib.auth.decorators import user_passes_test


def index(request):
	return render(request, 'frontend/index.html', {'DEBUG': settings.DEBUG})