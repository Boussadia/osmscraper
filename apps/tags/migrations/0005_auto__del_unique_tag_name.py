# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['name']
        db.delete_unique(u'tags_tag', ['name'])


    def backwards(self, orm):
        # Adding unique constraint on 'Tag', fields ['name']
        db.create_unique(u'tags_tag', ['name'])


    models = {
        u'tags.tag': {
            'Meta': {'unique_together': "(('name', 'is_super_tag'),)", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_super_tag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'stemmed_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        }
    }

    complete_apps = ['tags']