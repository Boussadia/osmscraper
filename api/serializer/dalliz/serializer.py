#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from django.contrib.auth.models import User

from rest_framework import serializers
from dalliz.models import Category, Brand

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

class CategoryURLField(serializers.CharField):
	def to_native(self, category):
		url = category.url
		if category.parent_category is not None:
			url = category.parent_category.url + '/'+ url
		return url

class CategorySerializer(serializers.ModelSerializer):
	url = CategoryURLField(source = '*')
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
			return Category.objects.filter(parent_category = category).order_by('position')
		else:
			return Category.objects.filter(parent_category__isnull = True).order_by('position')



class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ('password', 'groups', 'user_permissions')


class BrandSerializer(serializers.ModelSerializer):
	class Meta:
		model = Brand
