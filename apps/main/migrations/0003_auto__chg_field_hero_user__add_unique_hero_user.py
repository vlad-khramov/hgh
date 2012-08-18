# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Hero.user'
        db.alter_column('main_hero', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['auth.User']))
        # Adding unique constraint on 'Hero', fields ['user']
        db.create_unique('main_hero', ['user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Hero', fields ['user']
        db.delete_unique('main_hero', ['user_id'])


        # Changing field 'Hero.user'
        db.alter_column('main_hero', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

    models = {
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.hero': {
            'Meta': {'object_name': 'Hero'},
            'attack_github': ('django.db.models.fields.IntegerField', [], {}),
            'attack_own': ('django.db.models.fields.IntegerField', [], {}),
            'attentiveness_github': ('django.db.models.fields.IntegerField', [], {}),
            'attentiveness_own': ('django.db.models.fields.IntegerField', [], {}),
            'avatar_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'blog': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'charm_github': ('django.db.models.fields.IntegerField', [], {}),
            'charm_own': ('django.db.models.fields.IntegerField', [], {}),
            'defence_github': ('django.db.models.fields.IntegerField', [], {}),
            'defence_own': ('django.db.models.fields.IntegerField', [], {}),
            'experience': ('django.db.models.fields.IntegerField', [], {}),
            'followers': ('django.db.models.fields.IntegerField', [], {}),
            'following': ('django.db.models.fields.IntegerField', [], {}),
            'hireable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'html_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'losses': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'public_gists': ('django.db.models.fields.IntegerField', [], {}),
            'public_repos': ('django.db.models.fields.IntegerField', [], {}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'hero'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'wins': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.unit': {
            'Meta': {'object_name': 'Unit'},
            'attack_github': ('django.db.models.fields.IntegerField', [], {}),
            'attentiveness_github': ('django.db.models.fields.IntegerField', [], {}),
            'charm_github': ('django.db.models.fields.IntegerField', [], {}),
            'custom_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'defence_github': ('django.db.models.fields.IntegerField', [], {}),
            'forks': ('django.db.models.fields.IntegerField', [], {}),
            'hero': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'units'", 'to': "orm['main.Hero']"}),
            'html_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'open_issues': ('django.db.models.fields.IntegerField', [], {}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'watchers': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['main']