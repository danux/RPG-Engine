# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'WorldNode'
        db.create_table('world_worldnode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('description', self.gf('mcnulty.dashboard.fields.HtmlField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('world', ['WorldNode'])

        # Adding model 'Language'
        db.create_table('world_language', (
            ('worldnode_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['world.WorldNode'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('world', ['Language'])

        # Adding model 'Nation'
        db.create_table('world_nation', (
            ('worldnode_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['world.WorldNode'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('world', ['Nation'])

        # Adding model 'Town'
        db.create_table('world_town', (
            ('worldnode_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['world.WorldNode'], unique=True, primary_key=True)),
            ('nation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['world.Nation'])),
            ('is_newbie_friendly', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('world', ['Town'])

        # Adding model 'Race'
        db.create_table('world_race', (
            ('worldnode_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['world.WorldNode'], unique=True, primary_key=True)),
            ('traditions', self.gf('mcnulty.dashboard.fields.HtmlField')()),
            ('characteristics', self.gf('mcnulty.dashboard.fields.HtmlField')()),
            ('physical_appearence', self.gf('mcnulty.dashboard.fields.HtmlField')()),
            ('playing_tips', self.gf('mcnulty.dashboard.fields.HtmlField')()),
        ))
        db.send_create_signal('world', ['Race'])


    def backwards(self, orm):
        
        # Deleting model 'WorldNode'
        db.delete_table('world_worldnode')

        # Deleting model 'Language'
        db.delete_table('world_language')

        # Deleting model 'Nation'
        db.delete_table('world_nation')

        # Deleting model 'Town'
        db.delete_table('world_town')

        # Deleting model 'Race'
        db.delete_table('world_race')


    models = {
        'world.language': {
            'Meta': {'object_name': 'Language', '_ormbases': ['world.WorldNode']},
            'worldnode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['world.WorldNode']", 'unique': 'True', 'primary_key': 'True'})
        },
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
