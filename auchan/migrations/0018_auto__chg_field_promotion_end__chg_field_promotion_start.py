# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Promotion.end'
        db.alter_column(u'auchan_promotion', 'end', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Promotion.start'
        db.alter_column(u'auchan_promotion', 'start', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'Promotion.end'
        db.alter_column(u'auchan_promotion', 'end', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Promotion.start'
        db.alter_column(u'auchan_promotion', 'start', self.gf('django.db.models.fields.DateField')(null=True))

    models = {
        u'auchan.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Brand']", 'null': 'True'})
        },
        u'auchan.cart': {
            'Meta': {'object_name': 'Cart'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'osm': ('django.db.models.fields.CharField', [], {'default': "'auchan'", 'max_length': '9999'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auchan.Product']", 'through': u"orm['auchan.Cart_content']", 'symmetrical': 'False'})
        },
        u'auchan.cart_content': {
            'Meta': {'unique_together': "(('cart', 'product'),)", 'object_name': 'Cart_content'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Cart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'auchan.cart_history': {
            'Meta': {'object_name': 'Cart_history'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Cart']"}),
            'computed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'auchan.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'auchan_category_dalliz_category'", 'symmetrical': 'False', 'to': u"orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Category']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'})
        },
        u'auchan.history': {
            'Meta': {'ordering': "['product', '-created']", 'object_name': 'History'},
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Product']"}),
            'shipping_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.ShippingArea']", 'null': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        u'auchan.product': {
            'Meta': {'object_name': 'Product'},
            'avantages': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Brand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auchan.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'complement': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'auchan_product_dalliz_category'", 'symmetrical': 'False', 'to': u"orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_match': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'package_measure': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'package_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'package_unit': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'pratique': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'}),
            'stemmed_text': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'auchan_product_tag_dalliz_tag'", 'symmetrical': 'False', 'to': u"orm['tags.Tag']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auchan.Tag']", 'null': 'True', 'symmetrical': 'False'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Unit']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'valeur_nutritionnelle': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'auchan.promotion': {
            'Meta': {'unique_together': "(('reference', 'shipping_area'),)", 'object_name': 'Promotion'},
            'after': ('django.db.models.fields.FloatField', [], {}),
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'before': ('django.db.models.fields.FloatField', [], {}),
            'content': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auchan.Product']", 'symmetrical': 'False'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'shipping_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.ShippingArea']", 'null': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'u'", 'max_length': '1'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        u'auchan.shippingarea': {
            'Meta': {'object_name': 'ShippingArea'},
            'city_name': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shipping_area': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'postal_code': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'auchan.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'auchan.unit': {
            'Meta': {'object_name': 'Unit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'dalliz.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dalliz.Category']", 'null': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tags.Tag']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        u'tags.Tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['auchan']