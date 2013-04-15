from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from mturk.helper import MturkHelper 
from scrapers.base.basecrawler import BaseCrawler as Crawler



def index(request, key):
	response = {}
	assignmentId = None
	workerId = None
	hitId = None
	turkSubmitTo = None

	method = request.method
	parameters = getattr(request, method)


	if method == 'GET' or method == 'POST':
		if 'assignmentId' in parameters:
			assignmentId = parameters['assignmentId']
		
		if 'hitId' in parameters:
			hitId = parameters['hitId']

		if 'workerId' in parameters:
			workerId = parameters['workerId']

		if 'turkSubmitTo' in parameters:
			turkSubmitTo = parameters['turkSubmitTo']

	helper = MturkHelper(key = key)
	response = helper.dump()

	if request.method == 'POST':
		reference_result = request.POST['flagged']
		helper.save_result(reference_result, hitId, assignementId, workerId)
		crawler = Crawler()
		# Posting data to amazon mturk
		crawler.post(url = turkSubmitTo, data = response)

	return render(request, 'mturk/index.html', response)