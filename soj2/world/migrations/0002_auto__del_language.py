# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Language'
        db.delete_table('world_language')


    def backwards(self, orm):
        
        # Adding model 'Language'
        db.create_table('world_language', (
            ('worldnode_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['world.WorldNode'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('world', ['Language'])


    models = {
        'world.nation': {
            'Meta': {'object_name': 'Nation', '_ormbases': ['world.WorldNode']},
            'worldnode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['world.WorldNode']", 'unique': 'True', 'primary_key': 'True'})
        },
        'world.race': {
            'Meta': {'object_name': 'Race', '_ormbases': ['world.WorldNode']},
            'characteristics': ('mcnulty.dashboard.fields.HtmlField', [], {}),
            'physical_appearence': ('mcnulty.dashboard.fields.HtmlField', [], {}),
            'playing_tips': ('mcnulty.dashboard.fields.HtmlField', [], {}),
            'traditions': ('mcnulty.dashboard.fields.HtmlField', [], {}),
            'worldnode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['world.WorldNode']", 'unique': 'True', 'primary_key': 'True'})
        },
        'world.town': {
            'Meta': {'object_name': 'Town', '_ormbases': ['world.WorldNode']},
            'is_newbie_friendly': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'nation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['world.Nation']"}),
            'worldnode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['world.WorldNode']", 'unique': 'True', 'primary_key': 'True'})
        },
        'world.worldnode': {
            'Meta': {'object_name': 'WorldNode'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('mcnulty.dashboard.fields.HtmlField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['world']
