# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'History'
        db.create_table('auchan_history', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auchan.Product'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('shipping_area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auchan.ShippingArea'], null=True)),
            ('availability', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('html', self.gf('django.db.models.fields.TextField')(max_length=9999999999999999999999L, null=True)),
        ))
        db.send_create_signal('auchan', ['History'])

        # Adding model 'Unit'
        db.create_table('auchan_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('auchan', ['Unit'])

        # Adding model 'Product'
        db.create_table('auchan_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=9999, unique=True, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auchan.Brand'], null=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auchan.Unit'], null=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('exists', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('valeur_nutritionnelle', self.gf('django.db.models.fields.TextField')(null=True)),
            ('avantages', self.gf('django.db.models.fields.TextField')(null=True)),
            ('conservation', self.gf('django.db.models.fields.TextField')(null=True)),
            ('pratique', self.gf('django.db.models.fields.TextField')(null=True)),
            ('ingredients', self.gf('django.db.models.fields.TextField')(null=True)),
            ('complement', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
            ('html', self.gf('django.db.models.fields.TextField')(max_length=9999999999999999999999L, null=True)),
            ('package_quantity', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('package_measure', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('package_unit', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('auchan', ['Product'])

        # Adding M2M table for field categories on 'Product'
        db.create_table('auchan_product_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['auchan.product'], null=False)),
            ('category', models.ForeignKey(orm['auchan.category'], null=False))
        ))
        db.create_unique('auchan_product_categories', ['product_id', 'category_id'])

        # Adding model 'Brand'
        db.create_table('auchan_brand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('auchan', ['Brand'])

        # Adding model 'Promotion'
        db.create_table('auchan_promotion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=9999, unique=True, null=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='s', max_length=1)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('before', self.gf('django.db.models.fields.FloatField')()),
            ('after', self.gf('django.db.models.fields.FloatField')()),
            ('unit_price', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('start', self.gf('django.db.models.fields.DateField')(null=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True)),
            ('shipping_area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auchan.ShippingArea'], null=True)),
            ('availability', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('html', self.gf('django.db.models.fields.TextField')(max_length=9999999999999999999999L, null=True)),
        ))
        db.send_create_signal('auchan', ['Promotion'])

        # Adding M2M table for field content on 'Promotion'
        db.create_table('auchan_promotion_content', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('promotion', models.ForeignKey(orm['auchan.promotion'], null=False)),
            ('product', models.ForeignKey(orm['auchan.product'], null=False))
        ))
        db.create_unique('auchan_promotion_content', ['promotion_id', 'product_id'])

        # Adding unique constraint on 'Category', fields ['parent_category', 'name']
        db.create_unique('auchan_category', ['parent_category_id', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Category', fields ['parent_category', 'name']
        db.delete_unique('auchan_category', ['parent_category_id', 'name'])

        # Deleting model 'History'
        db.delete_table('auchan_history')

        # Deleting model 'Unit'
        db.delete_table('auchan_unit')

        # Deleting model 'Product'
        db.delete_table('auchan_product')

        # Removing M2M table for field categories on 'Product'
        db.delete_table('auchan_product_categories')

        # Deleting model 'Brand'
        db.delete_table('auchan_brand')

        # Deleting model 'Promotion'
        db.delete_table('auchan_promotion')

        # Removing M2M table for field content on 'Promotion'
        db.delete_table('auchan_promotion_content')


    models = {
        'auchan.brand': {
            'Meta': {'object_name': 'Brand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'auchan.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.Category']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'})
        },
        'auchan.history': {
            'Meta': {'object_name': 'History'},
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.Product']"}),
            'shipping_area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.ShippingArea']", 'null': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {})
        },
        'auchan.product': {
            'Meta': {'object_name': 'Product'},
            'avantages': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.Brand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auchan.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'complement': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'package_measure': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'package_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'package_unit': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'pratique': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.Unit']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'valeur_nutritionnelle': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'auchan.promotion': {
            'Meta': {'object_name': 'Promotion'},
            'after': ('django.db.models.fields.FloatField', [], {}),
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'before': ('django.db.models.fields.FloatField', [], {}),
            'content': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auchan.Product']", 'symmetrical': 'False'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'}),
            'shipping_area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.ShippingArea']", 'null': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'s'", 'max_length': '1'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        'auchan.shippingarea': {
            'Meta': {'object_name': 'ShippingArea'},
            'city_name': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shipping_area': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'postal_code': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'auchan.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['auchan']