from __future__ import absolute_import
from django import template
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Sum
from django.template.defaultfilters import floatformat
from openaid.projects import models as projects_models
from openaid.codelists import models as codelists_models
from openaid import contexts

register = template.Library()

@register.filter(is_safe=True)
def currency(amount):
    return intcomma(floatformat((amount or 0.0) * settings.OPENAID_MULTIPLIER, 0))

@register.filter
def unique(args):
    return set([a for a in args if a])

def _get_code_list_items(instance, model):
    if instance and isinstance(instance, model):
        return instance.get_children()
    return model.objects.root_nodes()

@register.inclusion_tag('commons/main_panel.html', takes_context=True)
def crs_stats(context, instance=None, year=None, show_map=True):

    start_year = contexts.START_YEAR
    end_year = contexts.END_YEAR
    year = int(year or context.get(contexts.YEAR_FIELD, None) or end_year)

    filters = {
        'year': year,
    }

    if instance:
        filters['%s__in' % instance.code_list] = instance.get_descendants_pks(include_self=True)

    sectors = _get_code_list_items(instance, codelists_models.Sector)
    # channels = _get_code_list_items(instance, codelists_models.Channel)
    # agencies = codelists_models.Agency.objects.all() if not instance else []
    agencies = codelists_models.Agency.objects.all() if not isinstance(instance, codelists_models.Agency) else []
    aid_types = _get_code_list_items(instance, codelists_models.AidType)

    statistify = lambda item: (item, item.get_total_commitment(**filters))
    cleaner = lambda items: filter(lambda x: x[1], sorted(map(statistify, items), key=tot_order, reverse=True))
    tot_order = lambda item: item[1]

    activities = projects_models.Activity.objects.all()
    if len(filters.keys()):
        activities = activities.filter(**filters)

    selected_fact = instance.code_list_facet if instance else None

    commitment_sum = activities.aggregate(Sum('commitment'))['commitment__sum']
    disbursements_sum = activities.aggregate(Sum('disbursement'))['disbursement__sum']

    ctx = {
        'selected_year': year,
        'selected_code_list': instance,
        'selected_facet': selected_fact,
        'start_year': start_year,
        'end_year': end_year,
        'sector_stats': cleaner(sectors),
        'agency_stats': cleaner(agencies),
        'aid_stats': cleaner(aid_types),
        'projects_count': activities.distinct('project').count(),
        'commitments_sum': commitment_sum,
        'disbursements_sum': disbursements_sum,
        'years': range(start_year, end_year + 1),
        'show_map': show_map,
    }

    ctx['columns'] = 3 if len(ctx['sector_stats']) and len(ctx['agency_stats']) and len(ctx['aid_stats']) else 2

    if not selected_fact:

        multi_projects = projects_models.AnnualFunds.objects.filter(year=year).aggregate(
            multi_commitments_sum=Sum('commitment'),
            multi_disbursements_sum=Sum('disbursement'),
        )

        ctx.update(multi_projects)

        ctx.update({
            'total_commitments_sum': multi_projects['multi_commitments_sum'] + commitment_sum,
            'total_disbursements_sum': multi_projects['multi_disbursements_sum'] + disbursements_sum,
        })

        ctx.update({
            'multi_stats': projects_models.AnnualFunds.objects.filter(year=year).select_related('organization'),
        })

        # for c in ['commitments_sum', 'disbursements_sum',]:
        #     ctx[c] = ctx[c] / 1000000.0
        #     ctx['total_%s' % c] = ctx['total_%s' % c] / 1000000.0
        #     ctx['multi_%s' % c] = ctx['multi_%s' % c] / 1000000.0

    return ctx