# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Product.has_match'
        db.delete_column(u'ooshop_product', 'has_match')

        # Adding field 'Product.processed'
        db.add_column(u'ooshop_product', 'processed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Product.has_match'
        db.add_column(u'ooshop_product', 'has_match',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Deleting field 'Product.processed'
        db.delete_column(u'ooshop_product', 'processed')


    models = {
        u'dalliz.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dalliz.Category']", 'null': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tags.Tag']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        u'dalliz.unit': {
            'Meta': {'object_name': 'Unit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        u'ooshop.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Brand']", 'null': 'True'})
        },
        u'ooshop.cart': {
            'Meta': {'object_name': 'Cart'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'osm': ('django.db.models.fields.CharField', [], {'default': "'ooshop'", 'max_length': '9999'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ooshop.Product']", 'through': u"orm['ooshop.Cart_content']", 'symmetrical': 'False'})
        },
        u'ooshop.cart_content': {
            'Meta': {'unique_together': "(('cart', 'product'),)", 'object_name': 'Cart_content'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Cart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'ooshop.cart_history': {
            'Meta': {'ordering': "['cart', '-created']", 'object_name': 'Cart_history'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Cart']"}),
            'computed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'ooshop.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_category_dalliz_category'", 'symmetrical': 'False', 'to': u"orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Category']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        u'ooshop.history': {
            'Meta': {'ordering': "['product', '-created']", 'object_name': 'History'},
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Product']"}),
            'shipping_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.ShippingArea']", 'null': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {})
        },
        u'ooshop.product': {
            'Meta': {'object_name': 'Product'},
            'avertissements': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Brand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ooshop.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'composition': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conseils': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_product_dalliz_category'", 'symmetrical': 'False', 'to': u"orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'goodie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'informations': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'origine': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'package_measure': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'package_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'package_unit': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'}),
            'stemmed_text': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_product_tag_dalliz_tag'", 'symmetrical': 'False', 'to': u"orm['tags.Tag']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Unit']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        u'ooshop.promotion': {
            'Meta': {'unique_together': "(('reference', 'shipping_area'),)", 'object_name': 'Promotion'},
            'after': ('django.db.models.fields.FloatField', [], {}),
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'before': ('django.db.models.fields.FloatField', [], {}),
            'content': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ooshop.Product']", 'symmetrical': 'False'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'shipping_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.ShippingArea']", 'null': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'s'", 'max_length': '1'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        u'ooshop.shippingarea': {
            'Meta': {'object_name': 'ShippingArea'},
            'city_name': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shipping_area': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'postal_code': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'ooshop.unit': {
            'Meta': {'object_name': 'Unit'},
            'dalliz_unit': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'ooshop_unit_dalliz_unit'", 'null': 'True', 'to': u"orm['dalliz.Unit']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'stemmed_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        }
    }

    complete_apps = ['ooshop']