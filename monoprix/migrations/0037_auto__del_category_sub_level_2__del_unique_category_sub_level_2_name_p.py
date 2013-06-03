# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Category_final', fields ['name', 'parent_category']
        db.delete_unique(u'monoprix_category_final', ['name', 'parent_category_id'])

        # Removing unique constraint on 'Category_sub_level_1', fields ['name', 'parent_category']
        db.delete_unique(u'monoprix_category_sub_level_1', ['name', 'parent_category_id'])

        # Removing unique constraint on 'Category_sub_level_2', fields ['name', 'parent_category']
        db.delete_unique(u'monoprix_category_sub_level_2', ['name', 'parent_category_id'])

        # Deleting model 'Category_sub_level_2'
        db.delete_table(u'monoprix_category_sub_level_2')

        # Deleting model 'Product'
        db.delete_table(u'monoprix_product')

        # Removing M2M table for field category on 'Product'
        db.delete_table('monoprix_product_category')

        # Deleting model 'Category_main'
        db.delete_table(u'monoprix_category_main')

        # Deleting model 'Category_sub_level_1'
        db.delete_table(u'monoprix_category_sub_level_1')

        # Deleting model 'Product_history'
        db.delete_table(u'monoprix_product_history')

        # Deleting model 'User'
        db.delete_table(u'monoprix_user')

        # Deleting model 'Category_final'
        db.delete_table(u'monoprix_category_final')

        # Removing M2M table for field dalliz_category on 'Category_final'
        db.delete_table('monoprix_category_final_dalliz_category')

        # Deleting model 'Brand'
        db.delete_table(u'monoprix_brand')

        # Adding model 'Cart_history'
        db.create_table(u'monoprix_cart_history', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('computed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'monoprix', ['Cart_history'])

        # Deleting field 'Cart.session_key'
        db.delete_column(u'monoprix_cart', 'session_key')

        # Adding field 'Cart.osm'
        db.add_column(u'monoprix_cart', 'osm',
                      self.gf('django.db.models.fields.CharField')(default='monoprix', max_length=9999),
                      keep_default=False)


        # Changing field 'Cart_content.product'
        db.alter_column(u'monoprix_cart_content', 'product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.NewProduct']))

    def backwards(self, orm):
        # Adding model 'Category_sub_level_2'
        db.create_table(u'monoprix_category_sub_level_2', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Category_sub_level_1'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'monoprix', ['Category_sub_level_2'])

        # Adding unique constraint on 'Category_sub_level_2', fields ['name', 'parent_category']
        db.create_unique(u'monoprix_category_sub_level_2', ['name', 'parent_category_id'])

        # Adding model 'Product'
        db.create_table(u'monoprix_product', (
            ('conseil', self.gf('django.db.models.fields.TextField')(null=True)),
            ('dalliz_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Product'], null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=9999, unique=True)),
            ('ingredients', self.gf('django.db.models.fields.TextField')(null=True)),
            ('dalliz_url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Brand'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('unit_price', self.gf('django.db.models.fields.FloatField')(null=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('valeur_nutritionnelle', self.gf('django.db.models.fields.TextField')(null=True)),
            ('conservation', self.gf('django.db.models.fields.TextField')(null=True)),
            ('promotion', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('composition', self.gf('django.db.models.fields.TextField')(null=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Unit'])),
        ))
        db.send_create_signal(u'monoprix', ['Product'])

        # Adding M2M table for field category on 'Product'
        db.create_table(u'monoprix_product_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'monoprix.product'], null=False)),
            ('category_final', models.ForeignKey(orm[u'monoprix.category_final'], null=False))
        ))
        db.create_unique(u'monoprix_product_category', ['product_id', 'category_final_id'])

        # Adding model 'Category_main'
        db.create_table(u'monoprix_category_main', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
        ))
        db.send_create_signal(u'monoprix', ['Category_main'])

        # Adding model 'Category_sub_level_1'
        db.create_table(u'monoprix_category_sub_level_1', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Category_main'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'monoprix', ['Category_sub_level_1'])

        # Adding unique constraint on 'Category_sub_level_1', fields ['name', 'parent_category']
        db.create_unique(u'monoprix_category_sub_level_1', ['name', 'parent_category_id'])

        # Adding model 'Product_history'
        db.create_table(u'monoprix_product_history', (
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Product'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('promotion', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'monoprix', ['Product_history'])

        # Adding model 'User'
        db.create_table(u'monoprix_user', (
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('sex', self.gf('django.db.models.fields.CharField')(default='', max_length=1)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, unique=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Cart'], null=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'monoprix', ['User'])

        # Adding model 'Category_final'
        db.create_table(u'monoprix_category_final', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Category_sub_level_2'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'monoprix', ['Category_final'])

        # Adding M2M table for field dalliz_category on 'Category_final'
        db.create_table(u'monoprix_category_final_dalliz_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category_final', models.ForeignKey(orm[u'monoprix.category_final'], null=False)),
            ('category_sub', models.ForeignKey(orm[u'dalliz.category_sub'], null=False))
        ))
        db.create_unique(u'monoprix_category_final_dalliz_category', ['category_final_id', 'category_sub_id'])

        # Adding unique constraint on 'Category_final', fields ['name', 'parent_category']
        db.create_unique(u'monoprix_category_final', ['name', 'parent_category_id'])

        # Adding model 'Brand'
        db.create_table(u'monoprix_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dalliz_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Brand'], null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
        ))
        db.send_create_signal(u'monoprix', ['Brand'])

        # Deleting model 'Cart_history'
        db.delete_table(u'monoprix_cart_history')

        # Adding field 'Cart.session_key'
        db.add_column(u'monoprix_cart', 'session_key',
                      self.gf('django.db.models.fields.CharField')(default='unnavailable', max_length=1000, unique=True),
                      keep_default=False)

        # Deleting field 'Cart.osm'
        db.delete_column(u'monoprix_cart', 'osm')


        # Changing field 'Cart_content.product'
        db.alter_column(u'monoprix_cart_content', 'product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Product']))

    models = {
        u'dalliz.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dalliz.Category']", 'null': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['apps.tags.Tag']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        u'dalliz.unit': {
            'Meta': {'object_name': 'Unit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        u'monoprix.cart': {
            'Meta': {'object_name': 'Cart'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'osm': ('django.db.models.fields.CharField', [], {'default': "'monoprix'", 'max_length': '9999'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['monoprix.NewProduct']", 'through': u"orm['monoprix.Cart_content']", 'symmetrical': 'False'})
        },
        u'monoprix.cart_content': {
            'Meta': {'unique_together': "(('cart', 'product'),)", 'object_name': 'Cart_content'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Cart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.NewProduct']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'monoprix.cart_history': {
            'Meta': {'object_name': 'Cart_history'},
            'computed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'monoprix.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_category_dalliz_category'", 'symmetrical': 'False', 'to': u"orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Category']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'})
        },
        u'monoprix.history': {
            'Meta': {'object_name': 'History'},
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.NewProduct']"}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Store']", 'null': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        u'monoprix.newbrand': {
            'Meta': {'object_name': 'NewBrand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.NewBrand']", 'null': 'True'})
        },
        u'monoprix.newproduct': {
            'Meta': {'object_name': 'NewProduct'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.NewBrand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['monoprix.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'composition': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conseil': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_product_dalliz_category'", 'symmetrical': 'False', 'to': u"orm['dalliz.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_match': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'package_measure': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'package_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'package_unit': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'}),
            'stemmed_text': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_product_tag_dalliz_tag'", 'symmetrical': 'False', 'to': u"orm['apps.tags.Tag']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Unit']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'valeur_nutritionnelle': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'monoprix.promotion': {
            'Meta': {'unique_together': "(('reference', 'store'),)", 'object_name': 'Promotion'},
            'after': ('django.db.models.fields.FloatField', [], {}),
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'before': ('django.db.models.fields.FloatField', [], {}),
            'content': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['monoprix.NewProduct']", 'symmetrical': 'False'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Store']", 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'s'", 'max_length': '1'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        u'monoprix.store': {
            'Meta': {'unique_together': "(('name', 'city_name', 'postal_code', 'address'),)", 'object_name': 'Store'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'chain': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'city_name': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'ctm': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'fax': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'icon': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infos': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'is_LAD': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'phone': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'postal_code': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'monoprix.unit': {
            'Meta': {'object_name': 'Unit'},
            'dalliz_unit': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_unit_dalliz_unit'", 'symmetrical': 'False', 'to': u"orm['dalliz.Unit']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'apps.tags.Tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['monoprix']