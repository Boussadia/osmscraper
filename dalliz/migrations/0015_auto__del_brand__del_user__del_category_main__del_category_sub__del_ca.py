# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Cart_content', fields ['cart', 'product']
        db.delete_unique(u'dalliz_cart_content', ['cart_id', 'product_id'])

        # Deleting model 'Brand'
        db.delete_table(u'dalliz_brand')

        # Deleting model 'User'
        db.delete_table(u'dalliz_user')

        # Deleting model 'Category_main'
        db.delete_table(u'dalliz_category_main')

        # Deleting model 'Category_sub'
        db.delete_table(u'dalliz_category_sub')

        # Deleting model 'Cart_content'
        db.delete_table(u'dalliz_cart_content')

        # Deleting model 'Cart'
        db.delete_table(u'dalliz_cart')

        # Deleting model 'Product'
        db.delete_table(u'dalliz_product')

        # Removing M2M table for field product_categories on 'Product'
        db.delete_table('dalliz_product_product_categories')

        # Adding field 'NewBrand.is_mdd'
        db.add_column(u'dalliz_newbrand', 'is_mdd',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Brand'
        db.create_table(u'dalliz_brand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
        ))
        db.send_create_signal('dalliz', ['Brand'])

        # Adding model 'User'
        db.create_table(u'dalliz_user', (
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('sex', self.gf('django.db.models.fields.CharField')(default='', max_length=1)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, unique=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Cart'], null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('dalliz', ['User'])

        # Adding model 'Category_main'
        db.create_table(u'dalliz_category_main', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
        ))
        db.send_create_signal('dalliz', ['Category_main'])

        # Adding model 'Category_sub'
        db.create_table(u'dalliz_category_sub', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Category_main'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('dalliz', ['Category_sub'])

        # Adding model 'Cart_content'
        db.create_table(u'dalliz_cart_content', (
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Product'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Cart'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('dalliz', ['Cart_content'])

        # Adding unique constraint on 'Cart_content', fields ['cart', 'product']
        db.create_unique(u'dalliz_cart_content', ['cart_id', 'product_id'])

        # Adding model 'Cart'
        db.create_table(u'dalliz_cart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session_key', self.gf('django.db.models.fields.CharField')(max_length=1000, unique=True)),
        ))
        db.send_create_signal('dalliz', ['Cart'])

        # Adding model 'Product'
        db.create_table(u'dalliz_product', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999, unique=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Brand'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('dalliz', ['Product'])

        # Adding M2M table for field product_categories on 'Product'
        db.create_table(u'dalliz_product_product_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['dalliz.product'], null=False)),
            ('category_sub', models.ForeignKey(orm['dalliz.category_sub'], null=False))
        ))
        db.create_unique(u'dalliz_product_product_categories', ['product_id', 'category_sub_id'])

        # Deleting field 'NewBrand.is_mdd'
        db.delete_column(u'dalliz_newbrand', 'is_mdd')


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
        u'dalliz.newbrand': {
            'Meta': {'object_name': 'NewBrand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mdd': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dalliz.NewBrand']", 'null': 'True'})
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