from django.contrib import admin
from . import models
from django_mptt_admin.admin import DjangoMpttAdmin

class HierarchicalCodeListAdmin(DjangoMpttAdmin):
    raw_id_fields = ('parent',)
    search_fields = ('name',)
    list_display = ('code', 'name',)

for code_list_model in models.CODE_LISTS:
    if 'parent' in code_list_model._meta.get_all_field_names():
        admin.site.register(code_list_model, HierarchicalCodeListAdmin)
    else:
        admin.site.register(code_list_model)