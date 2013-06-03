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
		text = ''.join(soup.findAll(text=True))
		text = ' '.join(text.split())
		self.text = text
	