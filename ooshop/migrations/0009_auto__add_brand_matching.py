# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brand_matching'
        db.create_table('ooshop_brand_matching', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('dalliz_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Brand'])),
            ('ooshop_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Brand'])),
        ))
        db.send_create_signal('ooshop', ['Brand_matching'])


    def backwards(self, orm):
        # Deleting model 'Brand_matching'
        db.delete_table('ooshop_brand_matching')


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
        },
        'ooshop.brand': {
            'Meta': {'object_name': 'Brand'},
            'dalliz_brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ooshop_brand_dalliz_brand'", 'null': 'True', 'to': "orm['dalliz.Brand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'ooshop.brand_matching': {
            'Meta': {'object_name': 'Brand_matching'},
            'dalliz_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Brand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ooshop_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Brand']"}),
            'score': ('django.db.models.fields.FloatField', [], {})
        },
        'ooshop.category_final': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_final'},
            'cookie': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_category_final_category_dalliz'", 'symmetrical': 'False', 'to': "orm['dalliz.Category_sub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Category_sub_level_2']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'ooshop.category_main': {
            'Meta': {'object_name': 'Category_main'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'ooshop.category_sub_level_1': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_sub_level_1'},
            'cookie': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Category_main']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'ooshop.category_sub_level_2': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_sub_level_2'},
            'cookie': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Category_sub_level_1']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'ooshop.product': {
            'Meta': {'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Brand']", 'null': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ooshop.Category_final']", 'null': 'True', 'symmetrical': 'False'}),
            'dalliz_product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ooshop_product_dalliz_product'", 'null': 'True', 'to': "orm['dalliz.Product']"}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Unit']", 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        'ooshop.product_history': {
            'Meta': {'object_name': 'Product_history'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Product']"}),
            'promotion': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'promotion_type': ('django.db.models.fields.CharField', [], {'max_length': '9999'}),
            'references': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_promotion_lot'", 'symmetrical': 'False', 'to': "orm['ooshop.Product']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {})
        },
        'ooshop.unit': {
            'Meta': {'object_name': 'Unit'},
            'dalliz_unit': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'ooshop_unit_dalliz_unit'", 'null': 'True', 'to': "orm['dalliz.Unit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['ooshop']