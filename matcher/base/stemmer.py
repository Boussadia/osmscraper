#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time

from bs4 import BeautifulSoup, Comment
import Stemmer

from ooshop.models import NewProduct as Product
from matcher.models import BaseWord, Stem
from osmscraper.unaccent import unaccent

class BaseHTMLStemmer(object):
	"""
		This class is responsible for stemming a sentence. It takes a html formated string, converts it to 
		a soup object, extract text the text and stems it.
	"""
	def __init__(self, html):
		self.html = html
		self.soup = BeautifulSoup(html, "lxml", from_encoding = 'utf-8')
		self.text = None
		self.stemmed_text = None

	def extract_text(self):
		"""
			Extracts text form beautifulsoup object.
		"""
		# Extracting comments
		soup = self.soup
		comments = soup.findAll(text=lambda text:isinstance(text, Comment))
		[comment.extract() for comment in comments]
		text = ''.join(soup.findAll(text=True))
		text = ' '.join(text.split())
		self.text = text

	def stem_text(self):
		"""
			This method is responsible for generating a text with words replaced by stems.
		"""
		if self.text is None:
			self.extract_text()
		text = self.text.lower()
		stems = []
		words = re.split(r'[^a-zA-Z0-9]+', unaccent(text))
		words = tuple([str(w) for w in words])
		new_words = []
		base_words = { unaccent(bw.text.lower()): unaccent(bw.stem.word.lower()) for bw in BaseWord.objects.raw("select * from matcher_baseword where unaccent(lower(matcher_baseword.text)) in %s", [words])}
		# Now we need to go through the base words and replace found words by stems in text
		for word in words:
			if word in base_words:
				new_words.append(base_words[word])
			else:
				new_words.append(word)

		# Reconstucting text and returning it
		return ' '.join(new_words)
		