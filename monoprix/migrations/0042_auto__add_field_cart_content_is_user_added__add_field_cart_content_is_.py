# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Cart_content.is_user_added'
        db.add_column(u'monoprix_cart_content', 'is_user_added',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Cart_content.is_match'
        db.add_column(u'monoprix_cart_content', 'is_match',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Cart_content.is_suggested'
        db.add_column(u'monoprix_cart_content', 'is_suggested',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Cart_content.is_user_set'
        db.add_column(u'monoprix_cart_content', 'is_user_set',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Cart_content.ooshop_content'
        db.add_column(u'monoprix_cart_content', 'ooshop_content',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='monoprix_ooshop_related_content', null=True, to=orm['ooshop.Cart_content']),
                      keep_default=False)

        # Adding field 'Cart_content.auchan_content'
        db.add_column(u'monoprix_cart_content', 'auchan_content',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='monoprix_auchan_related_content', null=True, to=orm['auchan.Cart_content']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Cart_content.is_user_added'
        db.delete_column(u'monoprix_cart_content', 'is_user_added')

        # Deleting field 'Cart_content.is_match'
        db.delete_column(u'monoprix_cart_content', 'is_match')

        # Deleting field 'Cart_content.is_suggested'
        db.delete_column(u'monoprix_cart_content', 'is_suggested')

        # Deleting field 'Cart_content.is_user_set'
        db.delete_column(u'monoprix_cart_content', 'is_user_set')

        # Deleting field 'Cart_content.ooshop_content'
        db.delete_column(u'monoprix_cart_content', 'ooshop_content_id')

        # Deleting field 'Cart_content.auchan_content'
        db.delete_column(u'monoprix_cart_content', 'auchan_content_id')


    models = {
        u'auchan.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Brand']", 'null': 'True'})
        },
        u'auchan.cart': {
            'Meta': {'object_name': 'Cart'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'osm': ('django.db.models.fields.CharField', [], {'default': "'auchan'", 'max_length': '9999'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auchan.Product']", 'through': u"orm['auchan.Cart_content']", 'symmetrical': 'False'})
        },
        u'auchan.cart_content': {
            'Meta': {'unique_together': "(('cart', 'product'),)", 'object_name': 'Cart_content'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Cart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_match': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_suggested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_user_added': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_user_set': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'monoprix_content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'auchan_monoprix_related_content'", 'null': 'True', 'to': u"orm['monoprix.Cart_content']"}),
            'ooshop_content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'auchan_ooshop_related_content'", 'null': 'True', 'to': u"orm['ooshop.Cart_content']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'auchan.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'auchan_category_dalliz_category'", 'symmetrical': 'False', 'to': u"orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Category']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'})
        },
        u'auchan.product': {
            'Meta': {'object_name': 'Product'},
            'avantages': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Brand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auchan.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'complement': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'auchan_product_dalliz_category'", 'symmetrical': 'False', 'to': u"orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'package_measure': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'package_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'package_unit': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'pratique': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'}),
            'stemmed_text': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'auchan_product_tag_dalliz_tag'", 'symmetrical': 'False', 'to': u"orm['apps.tags.Tag']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auchan.Tag']", 'null': 'True', 'symmetrical': 'False'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Unit']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'valeur_nutritionnelle': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'auchan.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'auchan.unit': {
            'Meta': {'object_name': 'Unit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
        u'monoprix.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Brand']", 'null': 'True'})
        },
        u'monoprix.cart': {
            'Meta': {'object_name': 'Cart'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'osm': ('django.db.models.fields.CharField', [], {'default': "'monoprix'", 'max_length': '9999'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['monoprix.Product']", 'through': u"orm['monoprix.Cart_content']", 'symmetrical': 'False'})
        },
        u'monoprix.cart_content': {
            'Meta': {'unique_together': "(('cart', 'product'),)", 'object_name': 'Cart_content'},
            'auchan_content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monoprix_auchan_related_content'", 'null': 'True', 'to': u"orm['auchan.Cart_content']"}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Cart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_match': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_suggested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_user_added': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_user_set': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ooshop_content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monoprix_ooshop_related_content'", 'null': 'True', 'to': u"orm['ooshop.Cart_content']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'monoprix.cart_history': {
            'Meta': {'ordering': "['cart', '-created']", 'object_name': 'Cart_history'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Cart']"}),
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
            'Meta': {'ordering': "['product', '-created']", 'object_name': 'History'},
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Product']"}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Store']", 'null': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        u'monoprix.product': {
            'Meta': {'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Brand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['monoprix.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'composition': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conseil': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_product_dalliz_category'", 'symmetrical': 'False', 'to': u"orm['dalliz.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'package_measure': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'package_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'package_unit': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'}),
            'stemmed_text': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_product_tag_dalliz_tag'", 'symmetrical': 'False', 'to': u"orm['apps.tags.Tag']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Unit']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'valeur_nutritionnelle': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'monoprix.promotion': {
            'Meta': {'ordering': "['-end']", 'unique_together': "(('reference', 'store'),)", 'object_name': 'Promotion'},
            'after': ('django.db.models.fields.FloatField', [], {}),
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'before': ('django.db.models.fields.FloatField', [], {}),
            'content': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['monoprix.Product']", 'symmetrical': 'False'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
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
        u'ooshop.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Brand']", 'null': 'True'})
        },
        u'ooshop.cart': {
            'Meta': {'object_name': 'Cart'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'osm': ('django.db.models.fields.CharField', [], {'default': "'ooshop'", 'max_length': '9999'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ooshop.Product']", 'through': u"orm['ooshop.Cart_content']", 'symmetrical': 'False'})
        },
        u'ooshop.cart_content': {
            'Meta': {'unique_together': "(('cart', 'product'),)", 'object_name': 'Cart_content'},
            'auchan_content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ooshop_auchan_related_content'", 'null': 'True', 'to': u"orm['auchan.Cart_content']"}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Cart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_match': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_suggested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_user_added': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_user_set': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'monoprix_content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ooshop_monoprix_related_content'", 'null': 'True', 'to': u"orm['monoprix.Cart_content']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'related_osm': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
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
        u'ooshop.product': {
            'Meta': {'object_name': 'Product'},
            'avertissements': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Brand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ooshop.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'composition': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conseils': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_product_dalliz_category'", 'symmetrical': 'False', 'to': u"orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'goodie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'}),
            'stemmed_text': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_product_tag_dalliz_tag'", 'symmetrical': 'False', 'to': u"orm['apps.tags.Tag']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Unit']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        u'ooshop.unit': {
            'Meta': {'object_name': 'Unit'},
            'dalliz_unit': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'ooshop_unit_dalliz_unit'", 'null': 'True', 'to': u"orm['dalliz.Unit']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'apps.tags.Tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'stemmed_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        }
    }

    complete_apps = ['monoprix']