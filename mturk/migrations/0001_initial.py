# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Task'
        db.create_table(u'mturk_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('osm_from', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('osm_to', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'mturk', ['Task'])

        # Adding unique constraint on 'Task', fields ['key', 'osm_from', 'osm_to', 'reference']
        db.create_unique(u'mturk_task', ['key', 'osm_from', 'osm_to', 'reference'])

        # Adding model 'ResultTask'
        db.create_table(u'mturk_resulttask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hitId', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('assignementId', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('workerId', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mturk.Task'])),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'mturk', ['ResultTask'])


    def backwards(self, orm):
        # Removing unique constraint on 'Task', fields ['key', 'osm_from', 'osm_to', 'reference']
        db.delete_unique(u'mturk_task', ['key', 'osm_from', 'osm_to', 'reference'])

        # Deleting model 'Task'
        db.delete_table(u'mturk_task')

        # Deleting model 'ResultTask'
        db.delete_table(u'mturk_resulttask')


    models = {
        u'mturk.resulttask': {
            'Meta': {'object_name': 'ResultTask'},
            'assignementId': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hitId': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mturk.Task']"}),
            'workerId': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'mturk.task': {
            'Meta': {'unique_together': "(('key', 'osm_from', 'osm_to', 'reference'),)", 'object_name': 'Task'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'osm_from': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'osm_to': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['mturk']