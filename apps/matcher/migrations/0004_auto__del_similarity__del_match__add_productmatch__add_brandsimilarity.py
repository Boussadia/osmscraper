# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Similarity'
        db.delete_table('matcher_similarity')

        # Deleting model 'Match'
        db.delete_table('matcher_match')

        # Adding model 'ProductMatch'
        db.create_table('matcher_productmatch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monoprix_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.NewProduct'], unique=True, null=True)),
            ('ooshop_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewProduct'], unique=True, null=True)),
            ('auchan_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auchan.Product'], unique=True, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('matcher', ['ProductMatch'])

        # Adding model 'BrandSimilarity'
        db.create_table('matcher_brandsimilarity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('query_name', self.gf('django.db.models.fields.TextField')()),
            ('index_name', self.gf('django.db.models.fields.TextField')()),
            ('monoprix_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.NewBrand'], null=True)),
            ('ooshop_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewBrand'], null=True)),
            ('auchan_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auchan.Brand'], null=True)),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('matcher', ['BrandSimilarity'])

        # Adding model 'BrandMatch'
        db.create_table('matcher_brandmatch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monoprix_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.NewBrand'], unique=True, null=True)),
            ('ooshop_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewBrand'], unique=True, null=True)),
            ('auchan_brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auchan.Brand'], unique=True, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('matcher', ['BrandMatch'])

        # Adding model 'ProductSimilarity'
        db.create_table('matcher_productsimilarity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('query_name', self.gf('django.db.models.fields.TextField')()),
            ('index_name', self.gf('django.db.models.fields.TextField')()),
            ('monoprix_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.NewProduct'], null=True)),
            ('ooshop_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewProduct'], null=True)),
            ('auchan_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auchan.Product'], null=True)),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('matcher', ['ProductSimilarity'])

        # Deleting field 'MatcherLog.osm'
        db.delete_column('matcher_matcherlog', 'osm')

        # Adding field 'MatcherLog.name'
        db.add_column('matcher_matcherlog', 'name',
                      self.gf('django.db.models.fields.TextField')(default=' '),
                      keep_default=False)

        # Adding field 'MatcherLog.type'
        db.add_column('matcher_matcherlog', 'type',
                      self.gf('django.db.models.fields.TextField')(default=' '),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Similarity'
        db.create_table('matcher_similarity', (
            ('monoprix_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.NewProduct'], null=True)),
            ('auchan_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auchan.Product'], null=True)),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ooshop_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewProduct'], null=True)),
            ('index_osm', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('query_osm', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('matcher', ['Similarity'])

        # Adding model 'Match'
        db.create_table('matcher_match', (
            ('ooshop_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewProduct'], unique=True, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('monoprix_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.NewProduct'], unique=True, null=True)),
            ('auchan_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auchan.Product'], unique=True, null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('matcher', ['Match'])

        # Deleting model 'ProductMatch'
        db.delete_table('matcher_productmatch')

        # Deleting model 'BrandSimilarity'
        db.delete_table('matcher_brandsimilarity')

        # Deleting model 'BrandMatch'
        db.delete_table('matcher_brandmatch')

        # Deleting model 'ProductSimilarity'
        db.delete_table('matcher_productsimilarity')

        # Adding field 'MatcherLog.osm'
        db.add_column('matcher_matcherlog', 'osm',
                      self.gf('django.db.models.fields.TextField')(default=' '),
                      keep_default=False)

        # Deleting field 'MatcherLog.name'
        db.delete_column('matcher_matcherlog', 'name')

        # Deleting field 'MatcherLog.type'
        db.delete_column('matcher_matcherlog', 'type')


    models = {
        'auchan.brand': {
            'Meta': {'object_name': 'Brand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'auchan.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'auchan_category_dalliz_category'", 'symmetrical': 'False', 'to': "orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.Category']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'})
        },
        'auchan.product': {
            'Meta': {'object_name': 'Product'},
            'avantages': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.Brand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auchan.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'complement': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'auchan_product_dalliz_category'", 'symmetrical': 'False', 'to': "orm['dalliz.Category']"}),
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
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'auchan_product_tag_dalliz_tag'", 'symmetrical': 'False', 'to': "orm['auchan.Tag']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auchan.Tag']", 'null': 'True', 'symmetrical': 'False'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.Unit']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'valeur_nutritionnelle': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'auchan.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'auchan.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'dalliz.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Category']", 'null': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tags.Tag']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        'dalliz.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        'matcher.baseword': {
            'Meta': {'object_name': 'BaseWord'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['matcher.Stem']"}),
            'text': ('django.db.models.fields.TextField', [], {'unique': 'True', 'null': 'True'})
        },
        'matcher.brandmatch': {
            'Meta': {'object_name': 'BrandMatch'},
            'auchan_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.Brand']", 'unique': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monoprix_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.NewBrand']", 'unique': 'True', 'null': 'True'}),
            'ooshop_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.NewBrand']", 'unique': 'True', 'null': 'True'})
        },
        'matcher.brandsimilarity': {
            'Meta': {'object_name': 'BrandSimilarity'},
            'auchan_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.Brand']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_name': ('django.db.models.fields.TextField', [], {}),
            'monoprix_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.NewBrand']", 'null': 'True'}),
            'ooshop_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.NewBrand']", 'null': 'True'}),
            'query_name': ('django.db.models.fields.TextField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {})
        },
        'matcher.matcherlog': {
            'Meta': {'object_name': 'MatcherLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.TextField', [], {})
        },
        'matcher.possiblematch': {
            'Meta': {'object_name': 'PossibleMatch'},
            'auchan_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.Product']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monoprix_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.NewProduct']", 'null': 'True'}),
            'ooshop_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.NewProduct']", 'null': 'True'})
        },
        'matcher.productmatch': {
            'Meta': {'object_name': 'ProductMatch'},
            'auchan_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.Product']", 'unique': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monoprix_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.NewProduct']", 'unique': 'True', 'null': 'True'}),
            'ooshop_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.NewProduct']", 'unique': 'True', 'null': 'True'})
        },
        'matcher.productsimilarity': {
            'Meta': {'object_name': 'ProductSimilarity'},
            'auchan_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auchan.Product']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_name': ('django.db.models.fields.TextField', [], {}),
            'monoprix_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.NewProduct']", 'null': 'True'}),
            'ooshop_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.NewProduct']", 'null': 'True'}),
            'query_name': ('django.db.models.fields.TextField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {})
        },
        'matcher.stem': {
            'Meta': {'object_name': 'Stem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'word': ('django.db.models.fields.TextField', [], {'unique': 'True', 'null': 'True'})
        },
        'monoprix.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_category_dalliz_category'", 'symmetrical': 'False', 'to': "orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Category']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'})
        },
        'monoprix.newbrand': {
            'Meta': {'object_name': 'NewBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.NewBrand']", 'null': 'True'})
        },
        'monoprix.newproduct': {
            'Meta': {'object_name': 'NewProduct'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.NewBrand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['monoprix.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'composition': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conseil': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_product_dalliz_category'", 'symmetrical': 'False', 'to': "orm['dalliz.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'package_measure': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'package_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'package_unit': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'}),
            'stemmed_text': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_product_tag_dalliz_tag'", 'symmetrical': 'False', 'to': "orm['tags.Tag']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Unit']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'valeur_nutritionnelle': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'monoprix.unit': {
            'Meta': {'object_name': 'Unit'},
            'dalliz_unit': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_unit_dalliz_unit'", 'symmetrical': 'False', 'to': "orm['dalliz.Unit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'ooshop.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_category_dalliz_category'", 'symmetrical': 'False', 'to': "orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Category']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'})
        },
        'ooshop.newbrand': {
            'Meta': {'object_name': 'NewBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'ooshop.newproduct': {
            'Meta': {'object_name': 'NewProduct'},
            'avertissements': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.NewBrand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ooshop.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'composition': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conseils': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_product_dalliz_category'", 'symmetrical': 'False', 'to': "orm['dalliz.Category']"}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'goodie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_product_tag_dalliz_tag'", 'symmetrical': 'False', 'to': "orm['tags.Tag']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Unit']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        'ooshop.unit': {
            'Meta': {'object_name': 'Unit'},
            'dalliz_unit': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'ooshop_unit_dalliz_unit'", 'null': 'True', 'to': "orm['dalliz.Unit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'tags.Tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['matcher']