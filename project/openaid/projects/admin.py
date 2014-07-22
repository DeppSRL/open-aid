from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from ..attachments.admin import PhotoInlineAdmin
from .models import Project, Activity, Markers, ChannelReported, Organization, AnnualFunds


def make_admin_link(instance, name_field=None):
    url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                          instance._meta.module_name),
                  args=(instance.id,))
    return format_html(u'<a href="{}">{}</a>', url, name_field or 'Edit')


class ActivityInlineAdmin(admin.TabularInline):
    can_delete = False
    extra = 0
    model = Activity
    fields = ['admin_link', 'number', 'title', ]
    readonly_fields = ['title', 'number', 'admin_link', ]

    def admin_link(self, instance):
        return make_admin_link(instance)

    def has_add_permission(self, request):
        return False


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInlineAdmin,
        ActivityInlineAdmin,
    ]

class ActivityAdmin(TranslationAdmin):
    codelists = ['recipient', 'agency', 'aid_type', 'channel', 'finance_type', 'sector']
    codelists_links = ['%s_link' % cl for cl in codelists]

    fieldsets = (
        (None, {
            'fields': ('project_link', 'year', 'title', 'number', 'description')
        }),
        ('Taxonomies', {
            'classes': ('collapse',),
            'fields': ('geography', 'report_type', 'flow_type', 'bi_multi', 'is_ftc', 'is_pba', 'is_investment', 'markers', 'channel_reported')
        }),
        ('Codelists', {
            'classes': ('collapse',),
            'fields': codelists_links
        }),
    )

    readonly_fields = ['project_link', 'markers', 'year', ] + codelists_links

    def project_link(self, instance):
        return make_admin_link(instance.project, unicode(instance.project))

def _codelist_link(codelist):
    def wrap(self, obj):
        return make_admin_link(getattr(obj, codelist), name_field=getattr(obj, codelist).name)
    wrap.short_description = codelist
    wrap.allow_tags = True
    return wrap

for cl in ActivityAdmin.codelists:
    fieldname = '%s_link' % cl
    setattr(ActivityAdmin, fieldname, _codelist_link(cl))

class AnnualFundsInlineAdmin(admin.TabularInline):
    model = AnnualFunds
    extra = 1

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [
        AnnualFundsInlineAdmin,
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Markers)
admin.site.register(ChannelReported)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(AnnualFunds)
