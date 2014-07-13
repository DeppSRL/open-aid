# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Question'
        db.create_table(u'faq_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('answer', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=128)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('protected', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'faq', ['Question'])


    def backwards(self, orm):
        # Deleting model 'Question'
        db.delete_table(u'faq_question')


    models = {
        u'faq.question': {
            'Meta': {'ordering': "['sort_order', 'created_on']", 'object_name': 'Question'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['faq']