# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category_main'
        db.create_table('telemarket_category_main', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('telemarket', ['Category_main'])

        # Adding model 'Category_sub_1'
        db.create_table('telemarket_category_sub_1', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['telemarket.Category_main'])),
        ))
        db.send_create_signal('telemarket', ['Category_sub_1'])

        # Adding unique constraint on 'Category_sub_1', fields ['name', 'parent_category']
        db.create_unique('telemarket_category_sub_1', ['name', 'parent_category_id'])

        # Adding model 'Category_sub_2'
        db.create_table('telemarket_category_sub_2', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['telemarket.Category_sub_1'])),
        ))
        db.send_create_signal('telemarket', ['Category_sub_2'])

        # Adding unique constraint on 'Category_sub_2', fields ['name', 'parent_category']
        db.create_unique('telemarket_category_sub_2', ['name', 'parent_category_id'])

        # Adding model 'Category_sub_3'
        db.create_table('telemarket_category_sub_3', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['telemarket.Category_sub_2'])),
        ))
        db.send_create_signal('telemarket', ['Category_sub_3'])

        # Adding unique constraint on 'Category_sub_3', fields ['name', 'parent_category']
        db.create_unique('telemarket_category_sub_3', ['name', 'parent_category_id'])

        # Adding model 'Category_final'
        db.create_table('telemarket_category_final', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['telemarket.Category_sub_3'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
        ))
        db.send_create_signal('telemarket', ['Category_final'])

        # Adding unique constraint on 'Category_final', fields ['name', 'parent_category']
        db.create_unique('telemarket_category_final', ['name', 'parent_category_id'])

        # Adding M2M table for field dalliz_category on 'Category_final'
        db.create_table('telemarket_category_final_dalliz_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category_final', models.ForeignKey(orm['telemarket.category_final'], null=False)),
            ('category_sub', models.ForeignKey(orm['dalliz.category_sub'], null=False))
        ))
        db.create_unique('telemarket_category_final_dalliz_category', ['category_final_id', 'category_sub_id'])

        # Adding model 'Unit'
        db.create_table('telemarket_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('telemarket', ['Unit'])

        # Adding model 'Promotion'
        db.create_table('telemarket_promotion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1000)),
        ))
        db.send_create_signal('telemarket', ['Promotion'])

        # Adding model 'Product'
        db.create_table('telemarket_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['telemarket.Unit'])),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('promotion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['telemarket.Promotion'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['telemarket.Category_final'])),
        ))
        db.send_create_signal('telemarket', ['Product'])

        # Adding unique constraint on 'Product', fields ['title', 'url', 'category']
        db.create_unique('telemarket_product', ['title', 'url', 'category_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Product', fields ['title', 'url', 'category']
        db.delete_unique('telemarket_product', ['title', 'url', 'category_id'])

        # Removing unique constraint on 'Category_final', fields ['name', 'parent_category']
        db.delete_unique('telemarket_category_final', ['name', 'parent_category_id'])

        # Removing unique constraint on 'Category_sub_3', fields ['name', 'parent_category']
        db.delete_unique('telemarket_category_sub_3', ['name', 'parent_category_id'])

        # Removing unique constraint on 'Category_sub_2', fields ['name', 'parent_category']
        db.delete_unique('telemarket_category_sub_2', ['name', 'parent_category_id'])

        # Removing unique constraint on 'Category_sub_1', fields ['name', 'parent_category']
        db.delete_unique('telemarket_category_sub_1', ['name', 'parent_category_id'])

        # Deleting model 'Category_main'
        db.delete_table('telemarket_category_main')

        # Deleting model 'Category_sub_1'
        db.delete_table('telemarket_category_sub_1')

        # Deleting model 'Category_sub_2'
        db.delete_table('telemarket_category_sub_2')

        # Deleting model 'Category_sub_3'
        db.delete_table('telemarket_category_sub_3')

        # Deleting model 'Category_final'
        db.delete_table('telemarket_category_final')

        # Removing M2M table for field dalliz_category on 'Category_final'
        db.delete_table('telemarket_category_final_dalliz_category')

        # Deleting model 'Unit'
        db.delete_table('telemarket_unit')

        # Deleting model 'Promotion'
        db.delete_table('telemarket_promotion')

        # Deleting model 'Product'
        db.delete_table('telemarket_product')


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
        'telemarket.category_final': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_final'},
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'telemarket_category_final_category_dalliz'", 'symmetrical': 'False', 'to': "orm['dalliz.Category_sub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['telemarket.Category_sub_3']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'telemarket.category_main': {
            'Meta': {'object_name': 'Category_main'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'telemarket.category_sub_1': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_sub_1'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['telemarket.Category_main']"})
        },
        'telemarket.category_sub_2': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_sub_2'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['telemarket.Category_sub_1']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'telemarket.category_sub_3': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_sub_3'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['telemarket.Category_sub_2']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'telemarket.product': {
            'Meta': {'unique_together': "(('title', 'url', 'category'),)", 'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['telemarket.Category_final']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'promotion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['telemarket.Promotion']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['telemarket.Unit']"}),
            'unit_price': ('django.db.models.fields.FloatField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'telemarket.promotion': {
            'Meta': {'object_name': 'Promotion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1000'})
        },
        'telemarket.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['telemarket']