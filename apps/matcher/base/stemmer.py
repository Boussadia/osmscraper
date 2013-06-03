#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time

from bs4 import BeautifulSoup, Comment

from ooshop.models import Product
from apps.matcher.models import BaseWord, Stem
from osmscraper.unaccent import unaccent

class Stemmer(object):
	"""
		This class is responsible for stemming a sentence.
	"""
	def __init__(self, text = ''):
		self.text = text
		self.stemmed_text = None

	def stem_text(self):
		"""
			This method is responsible for generating a text with words replaced by stems.
		"""
		text = self.text.lower()
		stems = []
		reg = re.compile('[^\w|0-9]+', re.U)
		words = reg.split(text)
		words = tuple([unicode(w) for w in words])
		new_words = []
		base_words = { bw.text.lower(): bw.stem.word.lower() for bw in BaseWord.objects.raw("select * from matcher_baseword where lower(matcher_baseword.text) in %s", [words])}
		# Now we need to go through the base words and replace found words by stems in text
		for word in words:
			if word in base_words:
				new_words.append(base_words[word])
			else:
				new_words.append(word)

		# Reconstucting text and returning it
		return ' '.join(new_words)

class BaseHTMLStemmer(Stemmer):
	"""
		This class is responsible for stemming a sentence. It takes a html formated string, converts it to 
		a soup object, extract text the text and stems it.
	"""
	def __init__(self, html):
		super(BaseHTMLStemmer, self).__init__()
		self.html = html
		self.soup = BeautifulSoup(html, "lxml", from_encoding = 'utf-8')

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
		return self

	def stem_text(self):
		"""
			This method is responsible for generating a text with words replaced by stems.
		"""
		if self.text is None or self.text == '':
			self.extract_text()
		text = self.text.lower()
		stems = []
		reg = re.compile('[^\w|0-9]+', re.U)
		words = reg.split(text)
		words = tuple([unicode(w) for w in words])
		new_words = []
		base_words = { bw.text.lower(): bw.stem.word.lower() for bw in BaseWord.objects.raw("select * from matcher_baseword where lower(matcher_baseword.text) in %s", [words])}
		# Now we need to go through the base words and replace found words by stems in text
		for word in words:
			if word in base_words:
				new_words.append(base_words[word])
			else:
				new_words.append(word)

		# Reconstucting text and returning it
		return ' '.join(new_words)
