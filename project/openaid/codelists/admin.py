from django.contrib import admin
from . import models
from django.db.models import Count
from django_mptt_admin.admin import DjangoMpttAdmin


class CodeListAdmin(admin.ModelAdmin):

    list_display = ('code', 'name', )
    extra_list_display = ()

    def  get_list_display(self, request):
        return super(CodeListAdmin, self).get_list_display(request) + self.extra_list_display


class ActivityCodeListAdmin(CodeListAdmin):

    extra_list_display = ('activities', )

    def activities(self, obj):
        return "%s" % obj.activity_count
    activities.short_description = 'Activities'
    activities.admin_order_field = 'activity_count'

    def activities(self, obj):
        return "%s" % obj.activity_count
    activities.short_description = 'Activities'
    activities.admin_order_field = 'activity_count'

    def queryset(self, request):
        return super(CodeListAdmin, self).queryset(request).annotate(activity_count=Count('activity'))


class HierarchicalCodeListAdmin(DjangoMpttAdmin, ActivityCodeListAdmin):
    extra_list_display = ActivityCodeListAdmin.extra_list_display + ('level', )
    raw_id_fields = ('parent',)
    search_fields = ('name', 'code', 'description')
    list_filter = ('level', )


class RecipientCodeListAdmin(HierarchicalCodeListAdmin):

    extra_list_display = HierarchicalCodeListAdmin.extra_list_display + (
        'income_group', 'iso_code', 'iso_alpha2', 'popolazione', 'crescita_popolazione', 'pil', 'pil_procapite',
    )
    list_filter = HierarchicalCodeListAdmin.list_filter + ('income_group', )


class DonorCodeListAdmin(CodeListAdmin):
    extra_list_display = ('group', )
    list_filter = ('group', )


class ChannelCodeListAdmin(HierarchicalCodeListAdmin):
    extra_list_display = HierarchicalCodeListAdmin.extra_list_display + ('acronym', )


class AgencyCodeListAdmin(CodeListAdmin):
    extra_list_display = CodeListAdmin.extra_list_display + ('acronym', 'donor')


# register all codelists
admin.site.register(models.Donor, DonorCodeListAdmin)
admin.site.register(models.Agency, ActivityCodeListAdmin)
admin.site.register(models.Recipient, RecipientCodeListAdmin)
admin.site.register(models.Channel, ChannelCodeListAdmin)
admin.site.register(models.FinanceType, HierarchicalCodeListAdmin)
admin.site.register(models.AidType, HierarchicalCodeListAdmin)
admin.site.register(models.Sector, HierarchicalCodeListAdmin)
