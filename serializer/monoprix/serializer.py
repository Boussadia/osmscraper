#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from rest_framework import serializers

from monoprix.models import Product, History
from serializer.dalliz.serializer import DallizBrandField

class DescriptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('description', 'ingredients', 'valeur_nutritionnelle', 'conservation', 'conseil', 'composition')

class PackageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('package_quantity', 'package_measure', 'package_unit')

class HistoryField(serializers.RelatedField):
	def to_native(self, history_set):
		osm_location = self.context['osm']['location']
		if osm_location is not None:
			histories = history_set.filter(store__id = int(osm_location))
		else:
			histories = history_set.filter(store__isnull = True)
		return [
			{
				'created': h.created,
				'price': h.price,
				'unit_price': h.price,
				'availability': h.availability,
				'store': osm_location
			}
			for h in histories]

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
				'store': histories[0].store,
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

# class ProductSerializer(serializers.ModelSerializer):
# 	brand = DallizBrandField()
# 	price = PriceField(source='history_set')
# 	promotions = serializers.PrimaryKeyRelatedField(many=True, source='promotion_set')
# 	package = PackageField(source='__dict__')

# 	class Meta:
# 		model = Product
# 		exclude = ('stemmed_text', 'html', 'has_match', 'exists', 'id', 'comment', 'categories', 'dalliz_category', 'tag', 'created', 'updated', 'package_quantity', 'package_measure', 'package_unit', 'description', 'ingredients', 'valeur_nutritionnelle', 'conservation', 'conseil', 'composition')
# 		depth = 1

class ProductSerializer(serializers.ModelSerializer):
	brand = DallizBrandField()
	history = HistoryField(source='history_set')
	package = PackageSerializer(source = '*')
	promotions = serializers.PrimaryKeyRelatedField(many=True, source='promotion_set')
	description = DescriptionSerializer(source = '*')
	osm_url = serializers.URLField(source = 'url')

	class Meta:
		model = Product
		exclude = ('url', 'package_quantity', 'package_measure', 'package_unit', 'description', 'ingredients', 'valeur_nutritionnelle', 'conservation', 'conseil', 'composition', 'stemmed_text', 'html', 'has_match', 'exists', 'id', 'comment', 'categories', 'dalliz_category', 'tag', 'created', 'updated')
		depth = 1

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