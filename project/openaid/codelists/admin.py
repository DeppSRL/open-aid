from django.contrib import admin
from . import models
from django.db.models import Count
from django_mptt_admin.admin import DjangoMpttAdmin


class CodeListAdmin(admin.ModelAdmin):

    list_display = ('code', 'name', 'activities', )

    def activities(self, obj):
        return "%s" % obj.activity_count
    activities.short_description = 'Activities'
    activities.admin_order_field = 'activity_count'

    def queryset(self, request):
        return super(CodeListAdmin, self).queryset(request).annotate(activity_count=Count('activity'))


class HierarchicalCodeListAdmin(DjangoMpttAdmin, CodeListAdmin):
    raw_id_fields = ('parent',)
    search_fields = ('name', 'code', 'description')
    list_filter = ('level', )


class RecipientCodeListAdmin(HierarchicalCodeListAdmin):

    list_display = HierarchicalCodeListAdmin.list_display + (
        'iso_code', 'iso_alpha2', 'popolazione', 'crescita_popolazione', 'pil', 'pil_procapite',
    )

# register all code list to admin
for code_list_model in models.CODE_LISTS:
    if 'parent' in code_list_model._meta.get_all_field_names():
        # it is a hierarchy
        if code_list_model.code_list == 'recipient':
            # exception fo recipient
            admin.site.register(code_list_model, RecipientCodeListAdmin)
        else:
            admin.site.register(code_list_model, HierarchicalCodeListAdmin)
    else:
        admin.site.register(code_list_model, CodeListAdmin)