# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Task.processed'
        db.add_column(u'mturk_task', 'processed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Task.processed'
        db.delete_column(u'mturk_task', 'processed')


    models = {
        u'mturk.resulttask': {
            'Meta': {'unique_together': "(('task', 'assignementId'),)", 'object_name': 'ResultTask'},
            'assignementId': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mturk.Task']"}),
            'workerId': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'mturk.task': {
            'Meta': {'unique_together': "(('key', 'osm_from', 'osm_to', 'reference'),)", 'object_name': 'Task'},
            'hitId': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'osm_from': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'osm_to': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['mturk']