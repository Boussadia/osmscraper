#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from apps.tags.models import Tag


class Unit(models.Model):
	name = models.CharField(max_length=10, unique=True)

	def __unicode__(self):
		return self.name

class Prospect(models.Model):
	mail = models.EmailField(unique = True)

	def __unicode__(self):
		return self.mail

class Category(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey('self', null = True)
	url = models.CharField(max_length=9999, null=True)
	position = models.IntegerField(default=0)
	tags = models.ManyToManyField(Tag)

	algorithm_process = models.BooleanField(default = True)

	class Meta:
		unique_together = ("name", "parent_category")

	def __unicode__(self):
		return self.name

class Brand(models.Model):
	name = models.CharField(max_length=100, unique=True)
	parent_brand = models.ForeignKey('self', null=True)
	is_mdd = models.BooleanField(default = False)

	def __unicode__(self):
		return self.name