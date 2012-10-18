# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category_main'
        db.create_table('coursengo_category_main', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
        ))
        db.send_create_signal('coursengo', ['Category_main'])

        # Adding model 'Category_sub_level_1'
        db.create_table('coursengo_category_sub_level_1', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coursengo.Category_main'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
        ))
        db.send_create_signal('coursengo', ['Category_sub_level_1'])

        # Adding unique constraint on 'Category_sub_level_1', fields ['name', 'parent_category']
        db.create_unique('coursengo_category_sub_level_1', ['name', 'parent_category_id'])

        # Adding model 'Category_final'
        db.create_table('coursengo_category_final', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coursengo.Category_sub_level_1'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
        ))
        db.send_create_signal('coursengo', ['Category_final'])

        # Adding unique constraint on 'Category_final', fields ['name', 'parent_category']
        db.create_unique('coursengo_category_final', ['name', 'parent_category_id'])

        # Adding M2M table for field dalliz_category on 'Category_final'
        db.create_table('coursengo_category_final_dalliz_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category_final', models.ForeignKey(orm['coursengo.category_final'], null=False)),
            ('category_sub', models.ForeignKey(orm['dalliz.category_sub'], null=False))
        ))
        db.create_unique('coursengo_category_final_dalliz_category', ['category_final_id', 'category_sub_id'])

        # Adding model 'Brand'
        db.create_table('coursengo_brand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('coursengo', ['Brand'])

        # Adding model 'Unit'
        db.create_table('coursengo_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('coursengo', ['Unit'])

        # Adding model 'Product'
        db.create_table('coursengo_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coursengo.Brand'])),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coursengo.Unit'])),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('promotion', self.gf('django.db.models.fields.FloatField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coursengo.Category_final'])),
        ))
        db.send_create_signal('coursengo', ['Product'])

        # Adding unique constraint on 'Product', fields ['title', 'url', 'category']
        db.create_unique('coursengo_product', ['title', 'url', 'category_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Product', fields ['title', 'url', 'category']
        db.delete_unique('coursengo_product', ['title', 'url', 'category_id'])

        # Removing unique constraint on 'Category_final', fields ['name', 'parent_category']
        db.delete_unique('coursengo_category_final', ['name', 'parent_category_id'])

        # Removing unique constraint on 'Category_sub_level_1', fields ['name', 'parent_category']
        db.delete_unique('coursengo_category_sub_level_1', ['name', 'parent_category_id'])

        # Deleting model 'Category_main'
        db.delete_table('coursengo_category_main')

        # Deleting model 'Category_sub_level_1'
        db.delete_table('coursengo_category_sub_level_1')

        # Deleting model 'Category_final'
        db.delete_table('coursengo_category_final')

        # Removing M2M table for field dalliz_category on 'Category_final'
        db.delete_table('coursengo_category_final_dalliz_category')

        # Deleting model 'Brand'
        db.delete_table('coursengo_brand')

        # Deleting model 'Unit'
        db.delete_table('coursengo_unit')

        # Deleting model 'Product'
        db.delete_table('coursengo_product')


    models = {
        'coursengo.brand': {
            'Meta': {'object_name': 'Brand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'coursengo.category_final': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_final'},
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'coursengo_category_final_category_dalliz'", 'symmetrical': 'False', 'to': "orm['dalliz.Category_sub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coursengo.Category_sub_level_1']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'coursengo.category_main': {
            'Meta': {'object_name': 'Category_main'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'coursengo.category_sub_level_1': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_sub_level_1'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coursengo.Category_main']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'coursengo.product': {
            'Meta': {'unique_together': "(('title', 'url', 'category'),)", 'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coursengo.Brand']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coursengo.Category_final']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'promotion': ('django.db.models.fields.FloatField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coursengo.Unit']"}),
            'unit_price': ('django.db.models.fields.FloatField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'coursengo.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Category_main']"})
        }
    }

    complete_apps = ['coursengo']