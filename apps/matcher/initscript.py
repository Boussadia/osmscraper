#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
	Populating the database of stems
"""
from __future__ import absolute_import # Import because of modules names

import os
import codecs

from apps.matcher.models import Stem
from apps.matcher.models import BaseWord


directory = os.path.dirname(os.path.realpath(__file__))

def populate_db(path):
	"""
		Populates stems database, use only once

		Input :
			- path (string) : path to file with stems
	"""
	stems_file = codecs.open(path, 'r', 'utf-8')
	relations = []
	for line in stems_file:
		r = line.split()
		if r[1] == '=':
			continue
		else:
			stem = r[1]
			word = r[0]
			# Getting database instance or creating it
			stem_db, created = Stem.objects.get_or_create(word = stem)
			base_word, created = BaseWord.objects.get_or_create(text = word, defaults = {'stem': stem_db})
			if not created:
				base_word.stem = stem_db
				base_word.save()

def main():
	path = '/'.join([directory, 'stems.txt'])
	populate_db(path)


if __name__=='__main__':
	main()