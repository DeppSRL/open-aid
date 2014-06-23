from django.contrib import admin
from openaid.crs import models

admin.site.register(models.Project)
admin.site.register(models.Activity)
admin.site.register(models.Markers)
admin.site.register(models.ChannelReported)

class HierarchicalCodeListAdmin(admin.ModelAdmin):
    raw_id_fields = ('parent',)
    search_fields = ('name',)
    list_display = ('code', 'name',)

for code_list_model in models.CODE_LIST_MODELS:
    if hasattr(code_list_model, 'parent'):
        admin.site.register(code_list_model, HierarchicalCodeListAdmin)
    else:
        admin.site.register(code_list_model)