# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stem'
        db.create_table('matcher_stem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word', self.gf('django.db.models.fields.TextField')(unique=True, null=True)),
        ))
        db.send_create_signal('matcher', ['Stem'])

        # Adding model 'BaseWord'
        db.create_table('matcher_baseword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(unique=True, null=True)),
            ('stem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.matcher.Stem'])),
        ))
        db.send_create_signal('matcher', ['BaseWord'])


    def backwards(self, orm):
        # Deleting model 'Stem'
        db.delete_table('matcher_stem')

        # Deleting model 'BaseWord'
        db.delete_table('matcher_baseword')


    models = {
        'apps.matcher.baseword': {
            'Meta': {'object_name': 'BaseWord'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['matcher.Stem']"}),
            'text': ('django.db.models.fields.TextField', [], {'unique': 'True', 'null': 'True'})
        },
        'apps.matcher.stem': {
            'Meta': {'object_name': 'Stem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'word': ('django.db.models.fields.TextField', [], {'unique': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['apps.matcher']