#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from rest_framework import serializers

from auchan.models import Product, History
from serializer.dalliz.serializer import DallizBrandField

class HistoryField(serializers.ModelSerializer):
	class Meta:
		model = History
		exclude = ('html','product')

class ProductSimpleSerializer(serializers.ModelSerializer):
	brand = DallizBrandField()
	history = HistoryField(many=True, source='history_set')
	promotions = serializers.PrimaryKeyRelatedField(many=True, source='promotion_set')

	class Meta:
		model = Product
		exclude = ('stemmed_text', 'html', 'has_match', 'exists', 'id', 'comment', 'categories', 'dalliz_category', 'tag', 'created', 'updated')
		depth = 1

class DescriptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('avantages', 'conservation', 'valeur_nutritionnelle', 'pratique', 'ingredients', 'complement')

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