from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db import connection, transaction
from django.db.models import Q

def test(request):
	response = {}
	if request.method == 'GET':
		if 'assignmentId' in request.GET:
			assignmentId = request.GET['assignmentId']
		else:
			assignmentId = None
		response['assignmentId'] = assignmentId
	return render(request, 'mturk/test.html', response)