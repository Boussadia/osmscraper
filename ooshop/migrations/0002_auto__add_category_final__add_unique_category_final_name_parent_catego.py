# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category_final'
        db.create_table('ooshop_category_final', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Category_sub_level_2'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
        ))
        db.send_create_signal('ooshop', ['Category_final'])

        # Adding M2M table for field dalliz_category on 'Category_final'
        db.create_table('ooshop_category_final_dalliz_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category_final', models.ForeignKey(orm['ooshop.category_final'], null=False)),
            ('category_sub', models.ForeignKey(orm['dalliz.category_sub'], null=False))
        ))
        db.create_unique('ooshop_category_final_dalliz_category', ['category_final_id', 'category_sub_id'])

        # Adding unique constraint on 'Category_final', fields ['name', 'parent_category']
        db.create_unique('ooshop_category_final', ['name', 'parent_category_id'])

        # Adding model 'Category_sub_level_2'
        db.create_table('ooshop_category_sub_level_2', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Category_sub_level_1'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
        ))
        db.send_create_signal('ooshop', ['Category_sub_level_2'])

        # Adding unique constraint on 'Category_sub_level_2', fields ['name', 'parent_category']
        db.create_unique('ooshop_category_sub_level_2', ['name', 'parent_category_id'])

        # Adding model 'Unit'
        db.create_table('ooshop_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('ooshop', ['Unit'])

        # Adding M2M table for field dalliz_unit on 'Unit'
        db.create_table('ooshop_unit_dalliz_unit', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_unit', models.ForeignKey(orm['ooshop.unit'], null=False)),
            ('to_unit', models.ForeignKey(orm['dalliz.unit'], null=False))
        ))
        db.create_unique('ooshop_unit_dalliz_unit', ['from_unit_id', 'to_unit_id'])

        # Adding model 'Product'
        db.create_table('ooshop_product', (
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=9999, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Brand'], null=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Unit'], null=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('dalliz_product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ooshop_product_dalliz_product', null=True, to=orm['dalliz.Product'])),
        ))
        db.send_create_signal('ooshop', ['Product'])

        # Adding M2M table for field category on 'Product'
        db.create_table('ooshop_product_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['ooshop.product'], null=False)),
            ('category_final', models.ForeignKey(orm['ooshop.category_final'], null=False))
        ))
        db.create_unique('ooshop_product_category', ['product_id', 'category_final_id'])

        # Adding model 'Brand'
        db.create_table('ooshop_brand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('dalliz_brand', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ooshop_brand_dalliz_brand', null=True, to=orm['dalliz.Brand'])),
        ))
        db.send_create_signal('ooshop', ['Brand'])

        # Adding model 'Category_main'
        db.create_table('ooshop_category_main', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
        ))
        db.send_create_signal('ooshop', ['Category_main'])

        # Adding model 'Product_history'
        db.create_table('ooshop_product_history', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Product'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('promotion_type', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('promotion', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('ooshop', ['Product_history'])

        # Adding M2M table for field references on 'Product_history'
        db.create_table('ooshop_product_history_references', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product_history', models.ForeignKey(orm['ooshop.product_history'], null=False)),
            ('product', models.ForeignKey(orm['ooshop.product'], null=False))
        ))
        db.create_unique('ooshop_product_history_references', ['product_history_id', 'product_id'])

        # Adding model 'Category_sub_level_1'
        db.create_table('ooshop_category_sub_level_1', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Category_main'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
        ))
        db.send_create_signal('ooshop', ['Category_sub_level_1'])

        # Adding unique constraint on 'Category_sub_level_1', fields ['name', 'parent_category']
        db.create_unique('ooshop_category_sub_level_1', ['name', 'parent_category_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Category_sub_level_1', fields ['name', 'parent_category']
        db.delete_unique('ooshop_category_sub_level_1', ['name', 'parent_category_id'])

        # Removing unique constraint on 'Category_sub_level_2', fields ['name', 'parent_category']
        db.delete_unique('ooshop_category_sub_level_2', ['name', 'parent_category_id'])

        # Removing unique constraint on 'Category_final', fields ['name', 'parent_category']
        db.delete_unique('ooshop_category_final', ['name', 'parent_category_id'])

        # Deleting model 'Category_final'
        db.delete_table('ooshop_category_final')

        # Removing M2M table for field dalliz_category on 'Category_final'
        db.delete_table('ooshop_category_final_dalliz_category')

        # Deleting model 'Category_sub_level_2'
        db.delete_table('ooshop_category_sub_level_2')

        # Deleting model 'Unit'
        db.delete_table('ooshop_unit')

        # Removing M2M table for field dalliz_unit on 'Unit'
        db.delete_table('ooshop_unit_dalliz_unit')

        # Deleting model 'Product'
        db.delete_table('ooshop_product')

        # Removing M2M table for field category on 'Product'
        db.delete_table('ooshop_product_category')

        # Deleting model 'Brand'
        db.delete_table('ooshop_brand')

        # Deleting model 'Category_main'
        db.delete_table('ooshop_category_main')

        # Deleting model 'Product_history'
        db.delete_table('ooshop_product_history')

        # Removing M2M table for field references on 'Product_history'
        db.delete_table('ooshop_product_history_references')

        # Deleting model 'Category_sub_level_1'
        db.delete_table('ooshop_category_sub_level_1')


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
        'ooshop.category_final': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_final'},
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Category_main']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'ooshop.category_sub_level_2': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_sub_level_2'},
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
            'promotion': ('django.db.models.fields.FloatField', [], {}),
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