#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

# Stems
class Stem(models.Model):
	word = models.TextField(null=True, unique = True)

	def __unicode__(self):
		return self.word

class BaseWord(models.Model):
	text = models.TextField(null=True, unique = True)
	stem = models.ForeignKey(Stem)

	def __unicode__(self):
		return '%s -> %s'%(self.text, self.stem)