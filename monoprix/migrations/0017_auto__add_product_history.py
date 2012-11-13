# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Product_history'
        db.create_table('monoprix_product_history', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Product'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Unit'])),
            ('promotion', self.gf('django.db.models.fields.CharField')(max_length=9999)),
        ))
        db.send_create_signal('monoprix', ['Product_history'])


    def backwards(self, orm):
        # Deleting model 'Product_history'
        db.delete_table('monoprix_product_history')


    models = {
        'dalliz.brand': {
            'Meta': {'object_name': 'Brand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'dalliz.category_main': {
            'Meta': {'object_name': 'Category_main'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'dalliz.category_sub': {
            'Meta': {'object_name': 'Category_sub'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Category_main']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        'dalliz.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        'monoprix.brand': {
            'Meta': {'object_name': 'Brand'},
            'dalliz_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Brand']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'monoprix.cart': {
            'Meta': {'object_name': 'Cart'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['monoprix.Product']", 'through': "orm['monoprix.Cart_content']", 'symmetrical': 'False'}),
            'session_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1000'})
        },
        'monoprix.cart_content': {
            'Meta': {'unique_together': "(('cart', 'product'),)", 'object_name': 'Cart_content'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Cart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'monoprix.category_final': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_final'},
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_category_final_category_dalliz'", 'symmetrical': 'False', 'to': "orm['dalliz.Category_sub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Category_sub_level_2']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'monoprix.category_main': {
            'Meta': {'object_name': 'Category_main'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'monoprix.category_sub_level_1': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_sub_level_1'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Category_main']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'monoprix.category_sub_level_2': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_sub_level_2'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Category_sub_level_1']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'monoprix.product': {
            'Meta': {'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Brand']"}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['monoprix.Category_final']", 'symmetrical': 'False'}),
            'composition': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conseil': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'dalliz_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'promotion': ('django.db.models.fields.CharField', [], {'max_length': '9999'}),
            'reference': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9999'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Unit']"}),
            'unit_price': ('django.db.models.fields.FloatField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'}),
            'valeur_nutritionnelle': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'monoprix.product_history': {
            'Meta': {'object_name': 'Product_history'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Product']"}),
            'promotion': ('django.db.models.fields.CharField', [], {'max_length': '9999'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Unit']"}),
            'unit_price': ('django.db.models.fields.FloatField', [], {})
        },
        'monoprix.unit': {
            'Meta': {'object_name': 'Unit'},
            'dalliz_unit': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_unit_dalliz_unit'", 'symmetrical': 'False', 'to': "orm['dalliz.Unit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'monoprix.user': {
            'Meta': {'object_name': 'User'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Cart']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'})
        }
    }

    complete_apps = ['monoprix']