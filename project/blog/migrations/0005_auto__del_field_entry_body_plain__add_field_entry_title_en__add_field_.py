# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Entry.body_plain'
        db.delete_column(u'blog_entry', 'body_plain')

        # Adding field 'Entry.title_en'
        db.add_column(u'blog_entry', 'title_en',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.title_it'
        db.add_column(u'blog_entry', 'title_it',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.abstract_en'
        db.add_column(u'blog_entry', 'abstract_en',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.abstract_it'
        db.add_column(u'blog_entry', 'abstract_it',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.body_en'
        db.add_column(u'blog_entry', 'body_en',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.body_it'
        db.add_column(u'blog_entry', 'body_it',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Entry.body_plain'
        raise RuntimeError("Cannot reverse this migration. 'Entry.body_plain' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Entry.body_plain'
        db.add_column(u'blog_entry', 'body_plain',
                      self.gf('django.db.models.fields.TextField')(),
                      keep_default=False)

        # Deleting field 'Entry.title_en'
        db.delete_column(u'blog_entry', 'title_en')

        # Deleting field 'Entry.title_it'
        db.delete_column(u'blog_entry', 'title_it')

        # Deleting field 'Entry.abstract_en'
        db.delete_column(u'blog_entry', 'abstract_en')

        # Deleting field 'Entry.abstract_it'
        db.delete_column(u'blog_entry', 'abstract_it')

        # Deleting field 'Entry.body_en'
        db.delete_column(u'blog_entry', 'body_en')

        # Deleting field 'Entry.body_it'
        db.delete_column(u'blog_entry', 'body_it')


    models = {
        u'blog.entry': {
            'Meta': {'ordering': "['-published_at']", 'object_name': 'Entry'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'abstract_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'abstract_it': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_it': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 29, 0, 0)'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_it': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['blog']