# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Renaming model 'NewBrand'
        db.rename_table('dalliz_newbrand', 'dalliz_brand')


    def backwards(self, orm):
        # Renaming model 'Brand'
        db.rename_table('dalliz_brand', 'dalliz_newbrand')


    models = {
        u'dalliz.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mdd': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dalliz.Brand']", 'null': 'True'})
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
        u'dalliz.prospect': {
            'Meta': {'object_name': 'Prospect'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'})
        },
        u'dalliz.unit': {
            'Meta': {'object_name': 'Unit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        u'tags.Tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['dalliz']