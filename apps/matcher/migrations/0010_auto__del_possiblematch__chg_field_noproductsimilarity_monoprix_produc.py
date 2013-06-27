# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'PossibleMatch'
        db.delete_table(u'matcher_possiblematch')


        # Changing field 'NoProductSimilarity.monoprix_product'
        db.alter_column(u'matcher_noproductsimilarity', 'monoprix_product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Product'], null=True))

        # Changing field 'NoProductSimilarity.ooshop_product'
        db.alter_column(u'matcher_noproductsimilarity', 'ooshop_product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Product'], null=True))

        # Changing field 'BrandSimilarity.ooshop_brand'
        db.alter_column(u'matcher_brandsimilarity', 'ooshop_brand_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Brand'], null=True))

        # Changing field 'BrandSimilarity.dalliz_brand'
        db.alter_column(u'matcher_brandsimilarity', 'dalliz_brand_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Brand'], null=True))

        # Changing field 'BrandSimilarity.monoprix_brand'
        db.alter_column(u'matcher_brandsimilarity', 'monoprix_brand_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Brand'], null=True))

        # Changing field 'ProductMatch.monoprix_product'
        db.alter_column(u'matcher_productmatch', 'monoprix_product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Product'], unique=True, null=True))

        # Changing field 'ProductMatch.ooshop_product'
        db.alter_column(u'matcher_productmatch', 'ooshop_product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Product'], unique=True, null=True))

        # Changing field 'BrandMatch.ooshop_brand'
        db.alter_column(u'matcher_brandmatch', 'ooshop_brand_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Brand'], null=True))

        # Changing field 'BrandMatch.dalliz_brand'
        db.alter_column(u'matcher_brandmatch', 'dalliz_brand_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Brand']))

        # Changing field 'BrandMatch.monoprix_brand'
        db.alter_column(u'matcher_brandmatch', 'monoprix_brand_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Brand'], null=True))

        # Changing field 'ProductSimilarity.ooshop_product'
        db.alter_column(u'matcher_productsimilarity', 'ooshop_product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Product'], null=True))

        # Changing field 'ProductSimilarity.monoprix_product'
        db.alter_column(u'matcher_productsimilarity', 'monoprix_product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.Product'], null=True))

    def backwards(self, orm):
        # Adding model 'PossibleMatch'
        db.create_table(u'matcher_possiblematch', (
            ('ooshop_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewProduct'], null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('monoprix_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.NewProduct'], null=True)),
            ('auchan_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auchan.Product'], null=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'matcher', ['PossibleMatch'])


        # Changing field 'NoProductSimilarity.monoprix_product'
        db.alter_column(u'matcher_noproductsimilarity', 'monoprix_product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.NewProduct'], null=True))

        # Changing field 'NoProductSimilarity.ooshop_product'
        db.alter_column(u'matcher_noproductsimilarity', 'ooshop_product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewProduct'], null=True))

        # Changing field 'BrandSimilarity.ooshop_brand'
        db.alter_column(u'matcher_brandsimilarity', 'ooshop_brand_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewBrand'], null=True))

        # Changing field 'BrandSimilarity.dalliz_brand'
        db.alter_column(u'matcher_brandsimilarity', 'dalliz_brand_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.NewBrand'], null=True))

        # Changing field 'BrandSimilarity.monoprix_brand'
        db.alter_column(u'matcher_brandsimilarity', 'monoprix_brand_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.NewBrand'], null=True))

        # Changing field 'ProductMatch.monoprix_product'
        db.alter_column(u'matcher_productmatch', 'monoprix_product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.NewProduct'], unique=True, null=True))

        # Changing field 'ProductMatch.ooshop_product'
        db.alter_column(u'matcher_productmatch', 'ooshop_product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewProduct'], unique=True, null=True))

        # Changing field 'BrandMatch.ooshop_brand'
        db.alter_column(u'matcher_brandmatch', 'ooshop_brand_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewBrand'], null=True))

        # Changing field 'BrandMatch.dalliz_brand'
        db.alter_column(u'matcher_brandmatch', 'dalliz_brand_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.NewBrand']))

        # Changing field 'BrandMatch.monoprix_brand'
        db.alter_column(u'matcher_brandmatch', 'monoprix_brand_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.NewBrand'], null=True))

        # Changing field 'ProductSimilarity.ooshop_product'
        db.alter_column(u'matcher_productsimilarity', 'ooshop_product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewProduct'], null=True))

        # Changing field 'ProductSimilarity.monoprix_product'
        db.alter_column(u'matcher_productsimilarity', 'monoprix_product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monoprix.NewProduct'], null=True))

    models = {
        u'auchan.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Brand']", 'null': 'True'})
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
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'auchan_product_tag_dalliz_tag'", 'symmetrical': 'False', 'to': u"orm['tags.Tag']"}),
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
        u'dalliz.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mdd': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dalliz.Brand']", 'null': 'True'})
        },
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
        u'matcher.baseword': {
            'Meta': {'object_name': 'BaseWord'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['matcher.Stem']"}),
            'text': ('django.db.models.fields.TextField', [], {'unique': 'True', 'null': 'True'})
        },
        u'matcher.brandmatch': {
            'Meta': {'unique_together': "(('dalliz_brand', 'auchan_brand'), ('dalliz_brand', 'ooshop_brand'), ('dalliz_brand', 'monoprix_brand'))", 'object_name': 'BrandMatch'},
            'auchan_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Brand']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dalliz.Brand']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monoprix_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Brand']", 'null': 'True'}),
            'ooshop_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Brand']", 'null': 'True'})
        },
        u'matcher.brandsimilarity': {
            'Meta': {'object_name': 'BrandSimilarity'},
            'auchan_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Brand']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dalliz_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dalliz.Brand']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_name': ('django.db.models.fields.TextField', [], {}),
            'monoprix_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Brand']", 'null': 'True'}),
            'ooshop_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Brand']", 'null': 'True'}),
            'query_name': ('django.db.models.fields.TextField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {})
        },
        u'matcher.matcherlog': {
            'Meta': {'object_name': 'MatcherLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.TextField', [], {})
        },
        u'matcher.noproductsimilarity': {
            'Meta': {'unique_together': "(('monoprix_product', 'ooshop_product'), ('monoprix_product', 'auchan_product'), ('ooshop_product', 'auchan_product'))", 'object_name': 'NoProductSimilarity'},
            'auchan_product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Product']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monoprix_product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Product']", 'null': 'True'}),
            'ooshop_product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Product']", 'null': 'True'})
        },
        u'matcher.productmatch': {
            'Meta': {'object_name': 'ProductMatch'},
            'auchan_product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Product']", 'unique': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monoprix_product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Product']", 'unique': 'True', 'null': 'True'}),
            'ooshop_product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Product']", 'unique': 'True', 'null': 'True'})
        },
        u'matcher.productsimilarity': {
            'Meta': {'object_name': 'ProductSimilarity'},
            'auchan_product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auchan.Product']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_name': ('django.db.models.fields.TextField', [], {}),
            'monoprix_product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Product']", 'null': 'True'}),
            'ooshop_product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ooshop.Product']", 'null': 'True'}),
            'query_name': ('django.db.models.fields.TextField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {})
        },
        u'matcher.stem': {
            'Meta': {'object_name': 'Stem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'word': ('django.db.models.fields.TextField', [], {'unique': 'True', 'null': 'True'})
        },
        u'monoprix.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Brand']", 'null': 'True'})
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
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_product_tag_dalliz_tag'", 'symmetrical': 'False', 'to': u"orm['tags.Tag']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monoprix.Unit']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'valeur_nutritionnelle': ('django.db.models.fields.TextField', [], {'null': 'True'})
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
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_product_tag_dalliz_tag'", 'symmetrical': 'False', 'to': u"orm['tags.Tag']"}),
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
        u'tags.Tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'stemmed_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        }
    }

    complete_apps = ['matcher']