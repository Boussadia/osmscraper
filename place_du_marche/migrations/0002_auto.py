# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field dalliz_unit on 'Unit'
        db.create_table('place_du_marche_unit_dalliz_unit', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_unit', models.ForeignKey(orm['place_du_marche.unit'], null=False)),
            ('to_unit', models.ForeignKey(orm['dalliz.unit'], null=False))
        ))
        db.create_unique('place_du_marche_unit_dalliz_unit', ['from_unit_id', 'to_unit_id'])


    def backwards(self, orm):
        # Removing M2M table for field dalliz_unit on 'Unit'
        db.delete_table('place_du_marche_unit_dalliz_unit')


    models = {
        'dalliz.category_main': {
            'Meta': {'object_name': 'Category_main'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'dalliz.category_sub': {
            'Meta': {'object_name': 'Category_sub'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Category_main']"})
        },
        'dalliz.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        'place_du_marche.brand': {
            'Meta': {'object_name': 'Brand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'place_du_marche.category_final': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_final'},
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'place_du_marche_category_final_category_dalliz'", 'symmetrical': 'False', 'to': "orm['dalliz.Category_sub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['place_du_marche.Category_sub']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'place_du_marche.category_main': {
            'Meta': {'object_name': 'Category_main'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'place_du_marche.category_sub': {
            'Meta': {'object_name': 'Category_sub'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['place_du_marche.Category_main']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'place_du_marche.product': {
            'Meta': {'unique_together': "(('title', 'url', 'category'),)", 'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['place_du_marche.Brand']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['place_du_marche.Category_final']"}),
            'full_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'promotion': ('django.db.models.fields.FloatField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['place_du_marche.Unit']"}),
            'unit_price': ('django.db.models.fields.FloatField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'place_du_marche.unit': {
            'Meta': {'object_name': 'Unit'},
            'dalliz_unit': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'place_du_marche_unit_dalliz_unit'", 'symmetrical': 'False', 'to': "orm['dalliz.Unit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['place_du_marche']