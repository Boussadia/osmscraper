from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from mturk.helper import MturkHelper 
from apps.scrapers.base.basecrawler import BaseCrawler as Crawler



def index(request, key):
	response = {}
	response['assignmentId'] = None
	response['workerId'] = None
	response['hitId'] = None
	response['turkSubmitTo'] = 'https://workersandbox.mturk.com/mturk/externalSubmit'
	response['key'] = key

	method = request.method
	parameters = getattr(request, method)

	if method == 'GET' or method == 'POST':
		if 'assignmentId' in parameters:
			response['assignmentId'] = parameters['assignmentId']
		
		if 'hitId' in parameters:
			response['hitId'] = parameters['hitId']

		if 'workerId' in parameters:
			response['workerId'] = parameters['workerId']

		if 'turkSubmitTo' in parameters:
			response['turkSubmitTo'] = unicode(parameters['turkSubmitTo']) + '/mturk/externalSubmit'

	helper = MturkHelper(key = key, hitid = response['hitId'])
	response['taskid'] = helper.save_task()
	response.update(helper.dump())
	#if response['assignmentId'] is not None and response['assignmentId'] != 'ASSIGNMENT_ID_NOT_AVAILABLE':
	#	helper.save_result(assignment = response['assignmentId'], workerId = response['workerId'])

	#if request.method == 'POST':
	#	reference_result = request.POST['flagged']
	#	response['flagged'] = reference_result
	#	helper.save_result(reference_result, response['hitId'], response['assignmentId'], response['workerId'])

	return render(request, 'mturk/index.html', response)
