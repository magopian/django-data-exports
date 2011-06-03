# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Format'
        db.create_table('data_exports_format', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mime', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('attachment', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('data_exports', ['Format'])

        # Adding field 'Export.export_format'
        db.add_column('data_exports_export', 'export_format', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data_exports.Format'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Format'
        db.delete_table('data_exports_format')

        # Deleting field 'Export.export_format'
        db.delete_column('data_exports_export', 'export_format_id')


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
            'export_format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data_exports.Format']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'data_exports.format': {
            'Meta': {'ordering': "['name']", 'object_name': 'Format'},
            'attachment': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['data_exports']
