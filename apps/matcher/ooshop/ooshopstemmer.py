#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, Comment

from apps.matcher.base.stemmer import BaseHTMLStemmer

class OoshopStemmer(BaseHTMLStemmer):
	"""
		Specific stemmer for ooshop
	"""

	def __init__(self, html):
		super(OoshopStemmer, self).__init__(html)

	def extract_text(self):
		"""
			Extracts text form beautifulsoup object.
		"""
		# Extracting comments
		soup = self.soup
		comments = soup.findAll(text=lambda text:isinstance(text, Comment))
		[comment.extract() for comment in comments]
		# Specific to ooshop -> extract annotiation paragraphe
		annotation = soup.find('p', {'class': 'annotationFinArticle'})
		if annotation:
			annotation.extract()
		# extract unnecessary information
		line = soup.find(id='ctl00_cphC_pn3T1_ctl01_pQte')
		if line:
			line.extract()
		line = soup.find(id='ctl00_cphC_pn3T1_ctl01_pPictoFraicheur')
		if line:
			line.extract()
		line = soup.find(id='ctl00_cphC_pn3T1_ctl01_ucAjoutListe_upDDL')
		if line:
			line.extract()

		text = ''.join(soup.findAll(text=True))
		text = ' '.join(text.split())
		self.text = text
	