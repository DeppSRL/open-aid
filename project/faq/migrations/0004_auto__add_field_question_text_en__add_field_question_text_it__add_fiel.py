# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Question.text_en'
        db.add_column(u'faq_question', 'text_en',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Question.text_it'
        db.add_column(u'faq_question', 'text_it',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Question.answer_en'
        db.add_column(u'faq_question', 'answer_en',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Question.answer_it'
        db.add_column(u'faq_question', 'answer_it',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Question.text_en'
        db.delete_column(u'faq_question', 'text_en')

        # Deleting field 'Question.text_it'
        db.delete_column(u'faq_question', 'text_it')

        # Deleting field 'Question.answer_en'
        db.delete_column(u'faq_question', 'answer_en')

        # Deleting field 'Question.answer_it'
        db.delete_column(u'faq_question', 'answer_it')


    models = {
        u'faq.question': {
            'Meta': {'ordering': "['sort_order', 'created_on']", 'object_name': 'Question'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'answer_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'answer_it': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'text_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'text_it': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['faq']