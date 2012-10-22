# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Product'
        db.create_table('dalliz_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Brand'])),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Unit'])),
        ))
        db.send_create_signal('dalliz', ['Product'])

        # Adding M2M table for field product_categories on 'Product'
        db.create_table('dalliz_product_product_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['dalliz.product'], null=False)),
            ('category_sub', models.ForeignKey(orm['dalliz.category_sub'], null=False))
        ))
        db.create_unique('dalliz_product_product_categories', ['product_id', 'category_sub_id'])

        # Adding unique constraint on 'Product', fields ['title', 'url']
        db.create_unique('dalliz_product', ['title', 'url'])

        # Adding model 'Unit'
        db.create_table('dalliz_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
        ))
        db.send_create_signal('dalliz', ['Unit'])


    def backwards(self, orm):
        # Removing unique constraint on 'Product', fields ['title', 'url']
        db.delete_unique('dalliz_product', ['title', 'url'])

        # Deleting model 'Product'
        db.delete_table('dalliz_product')

        # Removing M2M table for field product_categories on 'Product'
        db.delete_table('dalliz_product_product_categories')

        # Deleting model 'Unit'
        db.delete_table('dalliz_unit')


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
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Category_main']"})
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