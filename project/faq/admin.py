__author__ = 'guglielmo'
from django.contrib import admin
from models import Question

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'sort_order',
                    'created_on', 'status']
    list_editable = ['sort_order', 'status']
    list_filter = ['status', ]
    search_fields = ['text', 'answer', ]
    
admin.site.register(Question, QuestionAdmin)
