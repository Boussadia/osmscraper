from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db import connection, transaction
from django.db.models import Q

def test(request):
	response = {'test': 1}
	return render(request, 'mturk/test.html', response)