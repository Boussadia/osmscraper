# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Category_sub_level_1', fields ['name', 'parent_category']
        db.delete_unique(u'ooshop_category_sub_level_1', ['name', 'parent_category_id'])

        # Removing unique constraint on 'Category_sub_level_2', fields ['name', 'parent_category']
        db.delete_unique(u'ooshop_category_sub_level_2', ['name', 'parent_category_id'])

        # Removing unique constraint on 'Category_final', fields ['name', 'parent_category']
        db.delete_unique(u'ooshop_category_final', ['name', 'parent_category_id'])

        # Deleting model 'Category_final'
        db.delete_table(u'ooshop_category_final')

        # Removing M2M table for field dalliz_category on 'Category_final'
        db.delete_table('ooshop_category_final_dalliz_category')

        # Deleting model 'Brand_matching'
        db.delete_table(u'ooshop_brand_matching')

        # Deleting model 'Category_sub_level_2'
        db.delete_table(u'ooshop_category_sub_level_2')

        # Deleting model 'Monoprix_matching'
        db.delete_table(u'ooshop_monoprix_matching')

        # Deleting model 'Category_sub_level_1'
        db.delete_table(u'ooshop_category_sub_level_1')

        # Deleting model 'Brand'
        db.delete_table(u'ooshop_brand')

        # Removing M2M table for field dalliz_brand_m2m on 'Brand'
        db.delete_table('ooshop_brand_dalliz_brand_m2m')

        # Deleting model 'Category_main'
        db.delete_table(u'ooshop_category_main')

        # Deleting model 'Product_history'
        db.delete_table(u'ooshop_product_history')

        # Removing M2M table for field references on 'Product_history'
        db.delete_table('ooshop_product_history_references')

        # Deleting model 'Product'
        db.delete_table(u'ooshop_product')

        # Removing M2M table for field category on 'Product'
        db.delete_table('ooshop_product_category')

        # Adding model 'Cart_content'
        db.create_table(u'ooshop_cart_content', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Cart'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewProduct'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'ooshop', ['Cart_content'])

        # Adding unique constraint on 'Cart_content', fields ['cart', 'product']
        db.create_unique(u'ooshop_cart_content', ['cart_id', 'product_id'])

        # Adding model 'Cart_history'
        db.create_table(u'ooshop_cart_history', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('computed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'ooshop', ['Cart_history'])

        # Adding model 'Cart'
        db.create_table(u'ooshop_cart', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('osm', self.gf('django.db.models.fields.CharField')(default='ooshop', max_length=9999)),
        ))
        db.send_create_signal(u'ooshop', ['Cart'])


    def backwards(self, orm):
        # Removing unique constraint on 'Cart_content', fields ['cart', 'product']
        db.delete_unique(u'ooshop_cart_content', ['cart_id', 'product_id'])

        # Adding model 'Category_final'
        db.create_table(u'ooshop_category_final', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Category_sub_level_2'])),
            ('cookie', self.gf('django.db.models.fields.CharField')(max_length=10000, null=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'ooshop', ['Category_final'])

        # Adding M2M table for field dalliz_category on 'Category_final'
        db.create_table(u'ooshop_category_final_dalliz_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category_final', models.ForeignKey(orm[u'ooshop.category_final'], null=False)),
            ('category_sub', models.ForeignKey(orm[u'dalliz.category_sub'], null=False))
        ))
        db.create_unique(u'ooshop_category_final_dalliz_category', ['category_final_id', 'category_sub_id'])

        # Adding unique constraint on 'Category_final', fields ['name', 'parent_category']
        db.create_unique(u'ooshop_category_final', ['name', 'parent_category_id'])

        # Adding model 'Brand_matching'
        db.create_table(u'ooshop_brand_matching', (
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('ooshop_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Brand'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dalliz_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Brand'])),
        ))
        db.send_create_signal(u'ooshop', ['Brand_matching'])

        # Adding model 'Category_sub_level_2'
        db.create_table(u'ooshop_category_sub_level_2', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Category_sub_level_1'])),
            ('cookie', self.gf('django.db.models.fields.CharField')(max_length=10000, null=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'ooshop', ['Category_sub_level_2'])

        # Adding unique constraint on 'Category_sub_level_2', fields ['name', 'parent_category']
        db.create_unique(u'ooshop_category_sub_level_2', ['name', 'parent_category_id'])

        # Adding model 'Monoprix_matching'
        db.create_table(u'ooshop_monoprix_matching', (
            ('monoprix_product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matching_monoprix_ooshop', to=orm['monoprix.Product'])),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('ooshop_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Product'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'ooshop', ['Monoprix_matching'])

        # Adding model 'Category_sub_level_1'
        db.create_table(u'ooshop_category_sub_level_1', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Category_main'])),
            ('cookie', self.gf('django.db.models.fields.CharField')(max_length=10000, null=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'ooshop', ['Category_sub_level_1'])

        # Adding unique constraint on 'Category_sub_level_1', fields ['name', 'parent_category']
        db.create_unique(u'ooshop_category_sub_level_1', ['name', 'parent_category_id'])

        # Adding model 'Brand'
        db.create_table(u'ooshop_brand', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('dalliz_brand', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ooshop_brand_dalliz_brand', null=True, to=orm['dalliz.Brand'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'ooshop', ['Brand'])

        # Adding M2M table for field dalliz_brand_m2m on 'Brand'
        db.create_table(u'ooshop_brand_dalliz_brand_m2m', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_brand', models.ForeignKey(orm[u'ooshop.brand'], null=False)),
            ('to_brand', models.ForeignKey(orm[u'dalliz.brand'], null=False))
        ))
        db.create_unique(u'ooshop_brand_dalliz_brand_m2m', ['from_brand_id', 'to_brand_id'])

        # Adding model 'Category_main'
        db.create_table(u'ooshop_category_main', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
        ))
        db.send_create_signal(u'ooshop', ['Category_main'])

        # Adding model 'Product_history'
        db.create_table(u'ooshop_product_history', (
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Product'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('promotion_type', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('promotion', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'ooshop', ['Product_history'])

        # Adding M2M table for field references on 'Product_history'
        db.create_table(u'ooshop_product_history_references', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product_history', models.ForeignKey(orm[u'ooshop.product_history'], null=False)),
            ('product', models.ForeignKey(orm[u'ooshop.product'], null=False))
        ))
        db.create_unique(u'ooshop_product_history_references', ['product_history_id', 'product_id'])

        # Adding model 'Product'
        db.create_table(u'ooshop_product', (
            ('monoprix_product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ooshop_monoprix_product', null=True, to=orm['monoprix.Product'])),
            ('dalliz_product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ooshop_product_dalliz_product', null=True, to=orm['dalliz.Product'])),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=9999, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Brand'], null=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Unit'], null=True)),
        ))
        db.send_create_signal(u'ooshop', ['Product'])

        # Adding M2M table for field category on 'Product'
        db.create_table(u'ooshop_product_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'ooshop.product'], null=False)),
            ('category_final', models.ForeignKey(orm[u'ooshop.category_final'], null=False))
        ))
        db.create_unique(u'ooshop_product_category', ['product_id', 'category_final_id'])

        # Deleting model 'Cart_content'
        db.delete_table(u'ooshop_cart_content')

        # Deleting model 'Cart_history'
        db.delete_table(u'ooshop_cart_history')

        # Deleting model 'Cart'
        db.delete_table(u'ooshop_cart')


    models = {
        u'dalliz.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dalliz.Category']", 'null': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tags.Tag']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        u'dalliz.unit': {
            'Meta': {'object_name': 'Unit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        u'ooshop.cart': {
            'Meta': {'object_name': 'Cart'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'osm': ('django.db.models.fields.CharField', [], {'default': "'ooshop'", 'max_length': '9999'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ooshop.NewProduct']", 'through': u"orm['ooshop.Cart_content']", 'symmetrical': 'False'})
        },
        u'ooshop.cart_content': {
            'Meta': {'unique_together': "(('cart', 'product'),)", 'object_name': 'Cart_content'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Cart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.NewProduct']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'ooshop.cart_history': {
            'Meta': {'object_name': 'Cart_history'},
            'computed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'ooshop.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_category_dalliz_category'", 'symmetrical': 'False', 'to': u"orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Category']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        u'ooshop.history': {
            'Meta': {'object_name': 'History'},
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.NewProduct']"}),
            'shipping_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.ShippingArea']", 'null': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {})
        },
        u'ooshop.newbrand': {
            'Meta': {'object_name': 'NewBrand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.NewBrand']", 'null': 'True'})
        },
        u'ooshop.newproduct': {
            'Meta': {'object_name': 'NewProduct'},
            'avertissements': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.NewBrand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ooshop.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'composition': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conseils': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_product_dalliz_category'", 'symmetrical': 'False', 'to': u"orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'goodie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_match': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'informations': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'origine': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'package_measure': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'package_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'package_unit': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'}),
            'stemmed_text': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_product_tag_dalliz_tag'", 'symmetrical': 'False', 'to': u"orm['tags.Tag']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Unit']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        u'ooshop.promotion': {
            'Meta': {'unique_together': "(('reference', 'shipping_area'),)", 'object_name': 'Promotion'},
            'after': ('django.db.models.fields.FloatField', [], {}),
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'before': ('django.db.models.fields.FloatField', [], {}),
            'content': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ooshop.NewProduct']", 'symmetrical': 'False'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'shipping_area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.ShippingArea']", 'null': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'s'", 'max_length': '1'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        u'ooshop.shippingarea': {
            'Meta': {'object_name': 'ShippingArea'},
            'city_name': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shipping_area': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'postal_code': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'ooshop.unit': {
            'Meta': {'object_name': 'Unit'},
            'dalliz_unit': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'ooshop_unit_dalliz_unit'", 'null': 'True', 'to': u"orm['dalliz.Unit']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['ooshop']