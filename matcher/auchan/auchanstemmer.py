#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, Comment

from matcher.base.stemmer import BaseHTMLStemmer

class AuchanStemmer(BaseHTMLStemmer):
	"""
		Specific stemmer for auchan
	"""

	def __init__(self, html):
		super(AuchanStemmer, self).__init__(html)

	# def extract_text(self):
	# 	"""
	# 		Extracts text form beautifulsoup object.
	# 	"""
	# 	# Extracting comments
	# 	soup = self.soup
	# 	comments = soup.findAll(text=lambda text:isinstance(text, Comment))
	# 	[comment.extract() for comment in comments]
	# 	# Specific to monoprix -> extract annotiation paragraphe
	# 	annotation = soup.findAll('div', {'class': 'SubContent'})[-1] # Last element is annotation in html
	# 	if annotation:
	# 		annotation.extract()
	# 	# extract unnecessary button
	# 	print_button = soup.find('p',{'class', 'PrintBtn'})
	# 	if print_button:
	# 		print_button.extract()

	# 	text = ''.join(soup.findAll(text=True))
	# 	text = ' '.join(text.split())
	# 	self.text = text
	