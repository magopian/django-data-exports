# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Export'
        db.create_table('data_exports_export', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('display_labels', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('data_exports', ['Export'])

        # Adding model 'Column'
        db.create_table('data_exports_column', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('export', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data_exports.Export'])),
            ('column', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('data_exports', ['Column'])


    def backwards(self, orm):
        
        # Deleting model 'Export'
        db.delete_table('data_exports_export')

        # Deleting model 'Column'
        db.delete_table('data_exports_column')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'data_exports.column': {
            'Meta': {'object_name': 'Column'},
            'column': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'export': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data_exports.Export']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'data_exports.export': {
            'Meta': {'object_name': 'Export'},
            'display_labels': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['data_exports']
