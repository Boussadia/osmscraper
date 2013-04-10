#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from rest_framework import serializers

from auchan.models import Product, History, Promotion
from api.serializer.dalliz.serializer import DallizBrandField

def merge_history_promotion(history, promotion, limit = 5):
	"""
		This function merges 2 dict one representing a promotion, one representing a history, both have to be ordered.
	"""
	return sorted(history+promotion, key=(lambda item: item['end'] if 'end' in item else item['created']))[:limit][::-1]

class DescriptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('avantages', 'conservation', 'valeur_nutritionnelle', 'pratique', 'ingredients', 'complement')

class PackageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('package_quantity', 'package_measure', 'package_unit')

# class HistoryField(serializers.RelatedField):
# 	def to_native(self, history_set):
# 		osm_location = self.context['osm']['location']
# 		if osm_location is not None:
# 			histories = history_set.filter(shipping_area__id = int(osm_location))[:5]
# 		else:
# 			histories = history_set.filter(shipping_area__isnull = True)[:5]
# 		return [
# 			{
# 				'created': h.created,
# 				'price': h.price,
# 				'unit_price': h.price,
# 				'availability': h.availability,
# 				'shipping_area': osm_location
# 			}
# 			for h in histories]

class HistoryField(serializers.RelatedField):
	def to_native(self, product):
		history_set = product.history_set
		osm_location = self.context['osm']['location']
		if osm_location is not None:
			histories = history_set.filter(shipping_area__id = int(osm_location))[:5]
			promotions = product.promotion_set.filter(type = Promotion.SIMPLE, shipping_area__id = int(osm_location))[:5]
		else:
			histories = history_set.filter(shipping_area__isnull = True)[:5]
			promotions = product.promotion_set.filter(type = Promotion.SIMPLE, shipping_area__isnull = True)[:5]
		history_data = [
			{
				'is_promotion': False,
				'created': h.created,
				'price': h.price,
				'unit_price': h.price,
				'availability': h.availability,
				'store': osm_location
			}
			for h in histories]

		promotion_data = [{
			'is_promotion': True,
			'start': p.start,
			'end': p.end,
			'before': p.before,
			'price': p.after,
			'unit_price': p.unit_price,
			'availability': p.availability,
			'store': osm_location
		} for p in promotions]



		return merge_history_promotion(history_data, promotion_data)

class ProductSerializer(serializers.ModelSerializer):
	brand = DallizBrandField()
	history = HistoryField(source='*')
	package = PackageSerializer(source = '*')
	promotions = serializers.PrimaryKeyRelatedField(many=True, source='promotion_set')
	description = DescriptionSerializer(source = '*')
	osm_url = serializers.URLField(source = 'url')

	class Meta:
		model = Product
		exclude = ('url', 'avantages', 'conservation', 'valeur_nutritionnelle', 'pratique', 'ingredients', 'complement','package_quantity', 'package_measure', 'package_unit', 'stemmed_text', 'html', 'has_match', 'exists', 'id', 'comment', 'categories', 'dalliz_category', 'tag', 'created', 'updated')
		depth = 1

class HistorySerializer(serializers.ModelSerializer):
	# description = DescriptionSerializer(source = 'product')
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

class ScoreField(serializers.FloatField):
	def to_native(self, value):
		if 'score' in self.context:
			score = self.context['score']
			return score
		else:
			return None

class MatchField(serializers.BooleanField):
	def to_native(self, value):
		if 'matching' in self.context:
			return self.context['matching']
		else:
			return None

class RecommendationSerializer(serializers.ModelSerializer):
	"""

	"""
	brand = DallizBrandField(source = 'brand')
	osm_url = serializers.URLField(source = 'url')
	score = ScoreField(source='*')
	is_match = MatchField(source='*')
	class Meta:
		model = Product
		fields = ('brand', 'name', 'reference', 'score', 'osm_url', 'is_match')

