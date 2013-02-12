# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShippingArea'
        db.create_table('auchan_shippingarea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city_name', self.gf('django.db.models.fields.TextField')(null=True)),
            ('postal_code', self.gf('django.db.models.fields.TextField')(null=True)),
            ('is_shipping_area', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('auchan', ['ShippingArea'])


    def backwards(self, orm):
        # Deleting model 'ShippingArea'
        db.delete_table('auchan_shippingarea')


    models = {
        'auchan.shippingarea': {
            'Meta': {'object_name': 'ShippingArea'},
            'city_name': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shipping_area': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'postal_code': ('django.db.models.fields.TextField', [], {'null': 'True'})
        }
    }

    complete_apps = ['auchan']