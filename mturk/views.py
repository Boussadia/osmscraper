# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from mturk.helper import MturkHelper 
from scrapers.base.basecrawler import BaseCrawler as Crawler



def index(request, key):
	response = {}
	response['assignmentId'] = None
	response['workerId'] = None
	response['hitId'] = None
	response['turkSubmitTo'] = None
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

	logger.info('URl Submit To : %s'%(str(response['turkSubmitTo'])))

	helper = MturkHelper(key = key)
	response.update(helper.dump())

	if request.method == 'POST':
		reference_result = request.POST['flagged']
		helper.save_result(reference_result, response['hitId'], response['assignmentId'], response['workerId'])
		if response['turkSubmitTo'] is not None:
			crawler = Crawler()
			# Posting data to amazon mturk
			r, c = crawler.post(url = response['turkSubmitTo'], data = response)
			logging.info('Response to post (%d) :'%c)
			logging.info(r)

	return render(request, 'mturk/index.html', response)