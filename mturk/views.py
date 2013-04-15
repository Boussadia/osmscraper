from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from scrapers.base.basecrawler import BaseCrawler as Crawler



def test(request):
	response = {}
	if request.method == 'GET':
		if 'assignmentId' in request.GET:
			assignmentId = request.GET['assignmentId']
			hitId = request.GET['hitId']
		else:
			assignmentId = None
			hitId = None
		response['assignmentId'] = assignmentId
		response['hitId'] = hitId

	if request.method == 'POST':
		assignmentId = request.POST['assignmentId']
		hitId = request.POST['hitId']
		response['assignmentId'] = assignmentId
		response['hitId'] = hitId

		crawler = Crawler()
		# Posting data to amazon mturk
		crawler.post(url = 'https://workersandbox.mturk.com/mturk/externalSubmit', data = response)

	return render(request, 'mturk/test.html', response)