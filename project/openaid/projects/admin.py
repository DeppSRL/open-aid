from django.contrib import admin
from django.core.urlresolvers import reverse
from django import forms
from django.db.models import Count, Max
from django.utils.html import format_html
from django_select2 import ModelSelect2Field, Select2Widget
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from ..attachments.admin import PhotoInlineAdmin, DocumentInlineAdmin
from .models import Project, Activity, Markers, ChannelReported, Organization, AnnualFunds, Utl, Problem, \
    Report, NewProject, Initiative
from ..codelists import models as codelist_models


def make_admin_link(instance, name_field=None):
    url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                          instance._meta.module_name),
                  args=(instance.id,))
    return format_html(u'<a href="{}">{}</a>', url, name_field or 'Edit')


class BeautyTranslationAdmin(object):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


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


class ReportInlineProjectAdmin(TranslationStackedInline):
    extra = 0
    model = Report
    exclude = ['initiative',]


class ProblemInlineProjectAdmin(TranslationStackedInline):
    extra = 0
    model = Problem
    exclude = ['initiative',]


class ReportInlineInitiativeAdmin(TranslationStackedInline):
    extra = 0
    model = Report
    exclude = ['project',]


class ProblemInlineInitiativeAdmin(TranslationStackedInline):
    extra = 0
    model = Problem
    exclude = ['project',]




class InitiativeAdmin(TranslationAdmin, BeautyTranslationAdmin):
    model = Initiative
    # form = InitiativeAdminForm
    inlines = [
        ReportInlineInitiativeAdmin,
        ProblemInlineInitiativeAdmin,
        DocumentInlineAdmin,
        PhotoInlineAdmin,
    ]

    list_display = ('code', 'title', 'country', 'total_project_costs', 'loan_amount_approved', 'grant_amount_approved',
                    'show_projects_count', 'show_last_update')

    search_fields = ('code', 'title', 'description_temp', 'recipient_temp__name', 'start_year')

    # se l'utente e' una UTL mostra i recipient a lui associati
    # ed inoltre limita i sectors alle sole foglie ovvero esclude i sector "padre"
    def render_change_form(self, request, context, *args, **kwargs):
        if not request.user.is_superuser and request.user.utl:
            context['adminform'].form.fields['recipient_temp'].queryset = request.user.utl.recipient_set.all()
        else:
            context['adminform'].form.fields['recipient_temp'].queryset = codelist_models.Recipient.objects.all()

        context['adminform'].form.fields['sector'].queryset = codelist_models.Sector.objects.filter(children__isnull=True).order_by('code')
        return super(InitiativeAdmin, self).render_change_form(request, context, args, kwargs)

    def get_queryset(self, request):
        return super(InitiativeAdmin, self).get_queryset(request).select_related('report','problem').annotate(
            projects_count=Count('project'),
            projects_last_update=Max('project__last_update')
        )

    def show_projects_count(self, inst):
        return inst.projects_count

    show_projects_count.admin_order_field = 'projects_count'
    show_projects_count.short_description = 'Projects'

    def show_last_update(self, inst):
        return inst.projects_last_update

    show_last_update.admin_order_field = 'projects_last_update'
    show_last_update.short_description = 'Last Update'


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        widgets = {
            'beneficiaries': forms.Textarea(attrs={'rows': 2}),
            'outcome': forms.Textarea(attrs={'rows': 2}),
            'other_financiers': forms.Textarea(attrs={'rows': 2}),
            'location': forms.Textarea(attrs={'rows': 2}),
        }


class ProjectAdmin(TranslationAdmin, BeautyTranslationAdmin):
    form = ProjectAdminForm
    list_display = ('crsid', 'number', 'recipient', 'title', 'start_year', 'end_year', 'last_update')
    list_filter = ('has_focus', 'start_year', 'end_year', 'agency')
    list_select_related = ('recipient', )
    search_fields = ('crsid', 'title', 'description', 'recipient__name', 'start_year','number')
    ordering = ('-last_update', '-end_year', )
    readonly_fields = ['recipient', 'agency', 'aid_type', 'channel', 'finance_type', 'sector', 'markers', 'crsid']
    inlines = [
        ReportInlineProjectAdmin,
        ProblemInlineProjectAdmin,
        DocumentInlineAdmin,
        PhotoInlineAdmin,
    ]
    fieldsets = (
        (None, {
            'fields': ('crsid', 'number', 'title', 'description', )
        }),
        (None, {
            'fields': ('recipient', 'aid_type', 'outcome', 'sector', 'beneficiaries', 'beneficiaries_female',
                       'status', 'is_suspended', 'start_year', 'end_year', 'expected_start_year',
                       'expected_completion_year',
                       'total_project_costs', 'other_financiers', 'loan_amount_approved', 'grant_amount_approved',
                       'agency', 'counterpart_authority', 'email', 'location', )
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        fields = super(ProjectAdmin, self).get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            fields.append('title')
            fields.append('title_en')
            fields.append('title_it')
        return fields

    def get_list_display(self, request):
        list_display = super(ProjectAdmin, self).get_list_display(request)
        if request.user.is_superuser:
            return list_display
        return [x for x in list_display if x != 'has_focus']

    def get_list_filter(self, request):
        list_filter = super(ProjectAdmin, self).get_list_filter(request)
        if request.user.is_superuser:
            return list_filter
        return [x for x in list_filter if x != 'has_focus']

    def get_queryset(self, request):
        queryset = super(ProjectAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.utl is None:
            return queryset.none()
        return queryset.filter(recipient__in=request.user.utl.recipient_set.all())


class ActivityAdmin(TranslationAdmin, BeautyTranslationAdmin):
    codelists = ['recipient', 'agency', 'aid_type', 'channel', 'finance_type', 'sector']
    codelists_links = ['%s_link' % cl for cl in codelists]
    list_filter = ['year']
    search_fields = ['project__pk', 'project__title', 'project__crsid']

    fieldsets = (
        (None, {
            'fields': (
                'project_link', 'year', 'title', 'number', 'description', 'commitment', 'commitment_usd',
                'disbursement',
                'disbursement_usd')
        }),
        ('Taxonomies', {
            'classes': ('collapse',),
            'fields': (
                'geography', 'report_type', 'flow_type', 'bi_multi', 'is_ftc', 'is_pba', 'is_investment', 'markers',
                'channel_reported')
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


class CodelistSelect2Widget(Select2Widget):
    options = {
        'minimumResultsForSearch': 6, # Only applicable for single value select.
        'placeholder': '', # Empty text label
        'allowClear': True, # Not allowed when field is multiple since there each value has a clear button.
        'multiple': False, # Not allowed when attached to <select>
        'closeOnSelect': False,
        'width': '350px',
    }


class CodelistSelect2Field(ModelSelect2Field):
    widget = CodelistSelect2Widget


class NewProjectAdminForm(forms.ModelForm):
    recipient = CodelistSelect2Field(queryset=codelist_models.Recipient.objects, required=True)
    agency = CodelistSelect2Field(queryset=codelist_models.Agency.objects, required=False)
    channel = CodelistSelect2Field(queryset=codelist_models.Channel.objects, required=False)
    finance_type = CodelistSelect2Field(queryset=codelist_models.FinanceType.objects, required=False)
    aid_type = CodelistSelect2Field(queryset=codelist_models.AidType.objects, required=False)
    sector = ModelSelect2Field(queryset=codelist_models.Sector.objects, widget=Select2Widget(select2_options={
        'width': '350px',
    }), required=False)

    class Meta:
        model = NewProject


class NewProjectAdmin(TranslationAdmin, BeautyTranslationAdmin):
    model = NewProject
    form = NewProjectAdminForm
    fields = ('title', 'number', 'description', 'year', 'commitment', 'disbursement',
              'recipient', 'agency', 'aid_type', 'channel', 'finance_type', 'sector')
    list_filter = ('year', 'agency')
    list_display = ('title', 'year', 'number', 'recipient', 'agency')
    inlines = [
        PhotoInlineAdmin,
    ]

    def render_change_form(self, request, context, *args, **kwargs):
        if not request.user.is_superuser and request.user.utl:
            context['adminform'].form.fields['recipient'].queryset = request.user.utl.recipient_set.all()
        else:
            context['adminform'].form.fields['recipient'].queryset = codelist_models.Recipient.objects.all()
        context['adminform'].form.fields['aid_type'].queryset = codelist_models.AidType.objects.root_nodes()
        context['adminform'].form.fields['channel'].queryset = codelist_models.Channel.objects.root_nodes()
        context['adminform'].form.fields['finance_type'].queryset = codelist_models.FinanceType.objects.root_nodes()
        context['adminform'].form.fields['sector'].queryset = codelist_models.Sector.objects.root_nodes()
        return super(NewProjectAdmin, self).render_change_form(request, context, args, kwargs)

    def get_queryset(self, request):
        queryset = super(NewProjectAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.utl is None:
            return queryset.none()
        return queryset.filter(recipient__in=request.user.utl.recipient_set.all())


admin.site.register(Project, ProjectAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Utl, UtlAdmin)
admin.site.register(Markers)
admin.site.register(ChannelReported)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(AnnualFunds)
admin.site.register(NewProject, NewProjectAdmin)
admin.site.register(Initiative, InitiativeAdmin)