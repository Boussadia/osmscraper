#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from rest_framework import serializers
from dalliz.models import Category

class DallizBrandField(serializers.RelatedField):
	def to_native(self, value):
		brand_match = value.brandmatch_set.all()
		brand = {}
		if len(brand_match)>0:
			dalliz_brand = brand_match[0].dalliz_brand
			brand = {
				'name': dalliz_brand.name,
				'mdd':dalliz_brand.is_mdd,
				}
		return brand

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		exclude = ('tags',)

	@staticmethod
	def all(category = None):
		"""
			This class method return all category architecture.
		"""
		categories = CategorySerializer.get_subs_dalliz(category)
		serialized = []
		for c in categories:
			data = CategorySerializer(c).data
			data.update({
				'subs': CategorySerializer.all(c)
			})
			if len(data['subs'])>0:
				data['leave'] = False
			else:
				data['leave'] = True
			serialized.append(data)
		return serialized

	@staticmethod
	def get_subs_dalliz(category = None):
		if category:
			return Category.objects.filter(parent_category = category)
		else:
			return Category.objects.filter(parent_category__isnull = True)