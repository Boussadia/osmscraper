#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from rest_framework import serializers

from ooshop.models import Product, History
from serializer.dalliz.serializer import DallizBrandField

class HistoryField(serializers.ModelSerializer):
	class Meta:
		model = History
		exclude = ('html','product')

class PriceField(serializers.RelatedField):
	def to_native(self, history_set):
		# History set already ordered by date
		price = {}
		histories = history_set.all()[:1]
		if len(histories)>0:
			price = {
				'created': histories[0].created,
				'price': histories[0].price,
				'unit_price': histories[0].unit_price,
				'shipping_area': (lambda x: x.id if x is not None else x)(histories[0].shipping_area),
				'availability': histories[0].availability
			}
		return price

class PackageField(serializers.RelatedField):
	def to_native(self, value):
		package = {
			'package_quantity': value['package_quantity'],
			'package_measure': value['package_measure'],
			'package_unit': value['package_unit'],
		}
		return package

class ProductSimpleSerializer(serializers.ModelSerializer):
	# brand = DallizBrandField()
	# price = PriceField(source='history_set')
	promotions = serializers.PrimaryKeyRelatedField(many=True, source='promotion_set')
	# package = PackageField(source='__dict__')

	class Meta:
		model = Product
		exclude = ('package_quantity', 'package_measure', 'package_unit', 'informations', 'ingredients', 'conservation', 'conseils', 'composition', 'avertissements', 'goodie', 'origine', 'stemmed_text', 'html', 'has_match', 'exists', 'id', 'comment', 'categories', 'dalliz_category', 'tag', 'created', 'updated')
		depth = 1

class DescriptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('informations', 'ingredients', 'conservation', 'conseils', 'composition', 'avertissements')

class PackageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('package_quantity', 'package_measure', 'package_unit')

class HistorySerializer(serializers.ModelSerializer):
	description = DescriptionSerializer(source = 'product')
	package = PackageSerializer(source = 'product')
	brand = DallizBrandField(source = 'product.brand')
	reference = serializers.CharField(source = 'product.reference')
	unit = serializers.RelatedField(source = 'product.unit')
	osm_url = serializers.URLField(source = 'product.url')
	image_url = serializers.URLField(source = 'product.image_url')
	name = serializers.CharField(source = 'product.name')
	class Meta:
		model = History
		exclude = ('html','id', 'product')
