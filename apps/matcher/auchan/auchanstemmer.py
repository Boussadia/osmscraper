#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, Comment

from apps.matcher.base.stemmer import BaseHTMLStemmer

class AuchanStemmer(BaseHTMLStemmer):
	"""
		Specific stemmer for auchan
	"""

	def __init__(self, html):
		super(AuchanStemmer, self).__init__(html)

	def extract_text(self):
		"""
			Extracts text form beautifulsoup object.
		"""
		# Extracting comments
		soup = self.soup
		comments = soup.findAll(text=lambda text:isinstance(text, Comment))
		[comment.extract() for comment in comments]
		# extract product description
		description = soup.find(id='panel-infos-detaillees')
		text_description = ''
		if description:
			text_description = ''.join(description.findAll(text=True))
			text_description = ' '.join(text_description.split())
		# extract product head
		head = soup.find(id='produit-infos')
		# Remove add to cart buttons
		line = head.find('tr', {'class':'line-2'})
		if line:
			line.extract()
		text_head = ''
		if head:
			text_head = ''.join(head.findAll(text=True))
			text_head = ' '.join(text_head.split())
		self.text = text_head+' '+text_description
		return self
	