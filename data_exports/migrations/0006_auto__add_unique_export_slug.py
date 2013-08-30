# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Export', fields ['slug']
        db.create_unique(u'data_exports_export', ['slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'Export', fields ['slug']
        db.delete_unique(u'data_exports_export', ['slug'])


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data_exports.column': {
            'Meta': {'ordering': "['order']", 'object_name': 'Column'},
            'column': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'export': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_exports.Export']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'data_exports.export': {
            'Meta': {'object_name': 'Export'},
            'export_format': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_exports.Format']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'data_exports.format': {
            'Meta': {'ordering': "['name']", 'object_name': 'Format'},
            'file_ext': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['data_exports']