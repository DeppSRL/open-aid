# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Question.updated_on'
        db.delete_column(u'faq_question', 'updated_on')


    def backwards(self, orm):
        # Adding field 'Question.updated_on'
        db.add_column(u'faq_question', 'updated_on',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 30, 0, 0)),
                      keep_default=False)


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
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['faq']