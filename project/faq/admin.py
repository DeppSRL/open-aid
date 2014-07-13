from modeltranslation.admin import TranslationAdmin
from django.contrib import admin
from models import Question

__author__ = 'guglielmo'

class QuestionAdmin(TranslationAdmin):
    list_display = ['text', 'sort_order',
                    'created_on', 'status']
    list_editable = ['sort_order', 'status']
    list_filter = ['status', ]
    search_fields = ['text', 'answer', ]

admin.site.register(Question, QuestionAdmin)
