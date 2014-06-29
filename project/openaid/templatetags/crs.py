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

@register.inclusion_tag('commons/stats.html', takes_context=True)
def crs_stats(context, instance=None, year=None):

    start_year = contexts.START_YEAR
    end_year = contexts.END_YEAR
    year = int(year or context.get(contexts.YEAR_FIELD, None) or end_year)

    filters = {
        'year': year,
    }

    if instance:
        filters['%s__in' % instance.code_list] = instance.get_descendants_pks(include_self=True)

    sectors = _get_code_list_items(instance, codelists_models.Sector)
    channels = _get_code_list_items(instance, codelists_models.Channel)
    aid_types = _get_code_list_items(instance, codelists_models.AidType)

    statistify = lambda item: (item, item.get_total_commitment(**filters))
    tot_order = lambda item: item[1]

    activities = projects_models.Activity.objects.all()
    if len(filters.keys()):
        activities = activities.filter(**filters)

    ctx = {
        'selected_year': year,
        'selected_code_list': instance,
        'selected_facet': instance.code_list_facet if instance else None,
        'start_year': start_year,
        'end_year': end_year,
        'sector_stats': sorted(map(statistify, sectors), key=tot_order, reverse=True),
        'channel_stats': sorted(map(statistify, channels), key=tot_order, reverse=True),
        'aid_stats': sorted(map(statistify, aid_types), key=tot_order, reverse=True),
        'projects_count': activities.distinct('project').count(),
        'commitments_sum': activities.aggregate(Sum('commitment'))['commitment__sum'],
        'disbursements_sum': activities.aggregate(Sum('disbursement'))['disbursement__sum'],
        'years': range(start_year, end_year + 1),
    }

    return ctx