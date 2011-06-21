# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Character'
        db.create_table('characters_character', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.UserProfile'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['world.Race'])),
            ('hometown', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['world.Town'])),
            ('back_story', self.gf('django.db.models.fields.TextField')()),
            ('physical_appearence', self.gf('django.db.models.fields.TextField')()),
            ('gm_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('approved_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='approved_characters', null=True, to=orm['auth.User'])),
            ('date_approved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_submitted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('characters', ['Character'])

    def backwards(self, orm):
        
        # Deleting model 'Character'
        db.delete_table('characters_character')


    models = {
        'accounts.instantmessenger': {
            'Meta': {'object_name': 'InstantMessenger'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'accounts.instantmessengermembership': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'InstantMessengerMembership'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instant_messenger': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.InstantMessenger']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.UserProfile']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'accounts.socialnetwork': {
            'Meta': {'object_name': 'SocialNetwork'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'help_text': ('django.db.models.fields.TextField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_to_expression': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'accounts.socialnetworkmembership': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'SocialNetworkMembership'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_to_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'social_network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.SocialNetwork']"}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.UserProfile']"})
        },
        'accounts.userprofile': {
            'Meta': {'ordering': "['pen_name']", 'object_name': 'UserProfile'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'GB'", 'max_length': '150'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'english_first_language': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instant_messengers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['accounts.InstantMessenger']", 'null': 'True', 'through': "orm['accounts.InstantMessengerMembership']", 'blank': 'True'}),
            'pen_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'social_networks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['accounts.SocialNetwork']", 'null': 'True', 'through': "orm['accounts.SocialNetworkMembership']", 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'Europe/London'", 'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'characters.character': {
            'Meta': {'ordering': "['name']", 'object_name': 'Character'},
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'approved_characters'", 'null': 'True', 'to': "orm['auth.User']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.UserProfile']"}),
            'back_story': ('django.db.models.fields.TextField', [], {}),
            'date_approved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gm_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hometown': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['world.Town']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'physical_appearence': ('django.db.models.fields.TextField', [], {}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['world.Race']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'world.nation': {
            'Meta': {'object_name': 'Nation', '_ormbases': ['world.WorldNode']},
            'worldnode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['world.WorldNode']", 'unique': 'True', 'primary_key': 'True'})
        },
        'world.race': {
            'Meta': {'object_name': 'Race', '_ormbases': ['world.WorldNode']},
            'characteristics': ('mcnulty.dashboard.fields.HtmlField', [], {}),
            'physical_appearence': ('mcnulty.dashboard.fields.HtmlField', [], {}),
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

    complete_apps = ['characters']
