# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Category_sub.position'
        db.add_column('dalliz_category_sub', 'position',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Category_sub.position'
        db.delete_column('dalliz_category_sub', 'position')


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
            'Meta': {'unique_together': "(('title', 'url'),)", 'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Brand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dalliz.Category_sub']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Unit']"}),
            'unit_price': ('django.db.models.fields.FloatField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'dalliz.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        }
    }

    complete_apps = ['dalliz']