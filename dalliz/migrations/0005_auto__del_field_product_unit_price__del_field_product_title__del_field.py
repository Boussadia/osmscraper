# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Product', fields ['url', 'title']
        db.delete_unique('dalliz_product', ['url', 'title'])

        # Deleting field 'Product.unit_price'
        db.delete_column('dalliz_product', 'unit_price')

        # Deleting field 'Product.title'
        db.delete_column('dalliz_product', 'title')

        # Deleting field 'Product.unit'
        db.delete_column('dalliz_product', 'unit_id')

        # Adding unique constraint on 'Product', fields ['url']
        db.create_unique('dalliz_product', ['url'])


    def backwards(self, orm):
        # Removing unique constraint on 'Product', fields ['url']
        db.delete_unique('dalliz_product', ['url'])

        # Adding field 'Product.unit_price'
        db.add_column('dalliz_product', 'unit_price',
                      self.gf('django.db.models.fields.FloatField')(default=None),
                      keep_default=False)

        # Adding field 'Product.title'
        db.add_column('dalliz_product', 'title',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=1000),
                      keep_default=False)

        # Adding field 'Product.unit'
        db.add_column('dalliz_product', 'unit',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['dalliz.Unit']),
                      keep_default=False)

        # Adding unique constraint on 'Product', fields ['url', 'title']
        db.create_unique('dalliz_product', ['url', 'title'])


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
        'dalliz.product': {
            'Meta': {'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Brand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dalliz.Category_sub']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9999'})
        },
        'dalliz.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        }
    }

    complete_apps = ['dalliz']