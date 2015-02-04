from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline, TranslationStackedInline
from ..attachments.admin import PhotoInlineAdmin
from .models import Project, Activity, Markers, ChannelReported, Organization, AnnualFunds, Utl, Document, Problem, \
    Report


def make_admin_link(instance, name_field=None):
    url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                          instance._meta.module_name),
                  args=(instance.id,))
    return format_html(u'<a href="{}">{}</a>', url, name_field or 'Edit')


class ActivityInlineAdmin(admin.TabularInline):
    can_delete = False
    extra = 0
    model = Activity
    fields = ['admin_link', 'number', 'title', 'commitment', 'disbursement']
    readonly_fields = ['title', 'number', 'admin_link', 'commitment', 'disbursement']

    def admin_link(self, instance):
        return make_admin_link(instance, instance.year)

    def has_add_permission(self, request):
        return False


class ReportInlineAdmin(TranslationStackedInline):
    extra = 0
    model = Report

class ProblemInlineAdmin(TranslationStackedInline):
    extra = 0
    model = Problem

class DocumentInlineAdmin(TranslationTabularInline):
    extra = 1
    model = Document


class ProjectAdmin(TranslationAdmin):

    list_display = ('crsid', 'recipient', 'title', 'start_year', 'end_year', 'has_focus')
    list_filter = ('has_focus', 'start_year', 'end_year')
    list_select_related = ('recipient', )
    search_fields = ('crsid', 'title', 'description', 'recipient__name', 'start_year')
    ordering = ('-end_year', )
    readonly_fields = ['recipient', 'agency', 'aid_type', 'channel', 'finance_type', 'sector', 'markers']
    fieldsets = (
            (None, {
                'fields': ('title', 'description', )
            }),
            (None, {
                'fields': ('recipient', 'aid_type', 'outcome', 'beneficiaries', 'beneficiaries_female',
                           'status', 'is_suspended', 'start_year', 'end_year', 'expected_start_year', 'expected_completion_year',
                           'total_project_costs', 'other_financiers', 'load_amount_approved', 'grant_amount_approved',
                           'agency', 'counterpart_authority', 'email', 'location', )
            }),
        )
    # def get_fieldsets(self, request, obj=None):
    #     # if request.user.is_superuser:
    #     #     return super(ProjectAdmin, self).get_fieldsets(request, obj)
    #     return (
    #         (None, {
    #             'fields': ('title', 'description', )
    #         }),
    #         (None, {
    #             'fields': ('location', 'outcome', 'beneficiaries', 'beneficiaries_female', 'status', 'is_suspended', )
    #         })
    #     )

    inlines = [
        ReportInlineAdmin,
        ProblemInlineAdmin,
        DocumentInlineAdmin,
        PhotoInlineAdmin,
    ]

    def get_queryset(self, request):
        queryset = super(ProjectAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.utl is None:
            return queryset.none()
        return queryset.filter(recipient__in=request.user.utl.recipient_set.all())

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


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

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

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


class RecipientInline(admin.TabularInline):
    model = Utl.recipient_set.through
    extra = 0
    allow_add = True


class UtlAdmin(admin.ModelAdmin):
    model = Utl
    fields = ('name', 'nation', 'city', 'user')
    list_display = ('name', 'nation', 'city', 'user')
    inlines = [
        RecipientInline,
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Utl, UtlAdmin)
admin.site.register(Markers)
admin.site.register(ChannelReported)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(AnnualFunds)
