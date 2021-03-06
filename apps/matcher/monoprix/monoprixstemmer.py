#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, Comment

from apps.matcher.base.stemmer import BaseHTMLStemmer

class MonoprixStemmer(BaseHTMLStemmer):
	"""
		Specific stemmer for monoprix
	"""

	def __init__(self, html):
		super(MonoprixStemmer, self).__init__(html)

	def extract_text(self):
		"""
			Extracts text form beautifulsoup object.
		"""
		# Extracting comments
		soup = self.soup
		comments = soup.findAll(text=lambda text:isinstance(text, Comment))
		[comment.extract() for comment in comments]
		# Specific to monoprix -> extract annotiation paragraphe
		annotation = soup.findAll('div', {'class': 'SubContent'})[-1] # Last element is annotation in html
		if annotation:
			annotation.extract()
		# extract unnecessary button
		print_button = soup.find('p',{'class', 'PrintBtn'})
		if print_button:
			print_button.extract()

		# extract unnecessary button
		print_button = soup.find('p',{'class', 'BackBtn'})
		if print_button:
			print_button.extract()

		# extract unnecessary information
		line = soup.find('div',{'class' :'ProductBuyingControl'})
		if line:
			line.extract()
		line = soup.find('div',{'class' :'Col01'})
		if line:
			line.extract()

		text = ''.join(soup.findAll(text=True))
		text = ' '.join(text.split())
		self.text = text
		return self