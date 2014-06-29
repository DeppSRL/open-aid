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

@register.inclusion_tag('commons/stats.html', takes_context=True)
def crs_stats(context, **kwargs):

    start_year = contexts.START_YEAR
    end_year = contexts.END_YEAR
    selected_year = context.get(contexts.YEAR_FIELD, None) or end_year

    filters = {
        'year': selected_year,
        }

    recipient = kwargs.get('recipient', None)
    if recipient:
        filters['recipient__in'] = recipient.get_descendants_pks(include_self=True)

    selected = selected_facet = None

    sector = kwargs.get('sector', None)
    if sector:
        filters['sector__in'] = sector.get_descendants_pks(include_self=True)
        selected = sector
        selected_facet = 'sectors'

    channel = kwargs.get('channel', None)
    if channel:
        filters['channel__in'] = channel.get_descendants_pks(include_self=True)
        selected = channel
        selected_facet = 'channels'

    aid = kwargs.get('aid', None)
    if aid:
        filters['aid_type__in'] = aid.get_descendants_pks(include_self=True)
        selected = aid
        selected_facet = 'aid_types'

    sectors = sector.children.all() if sector else codelists_models.Sector.objects.root_nodes()
    channels = channel.children.all() if channel else codelists_models.Channel.objects.root_nodes()
    aids = aid.children.all() if aid else codelists_models.AidType.objects.root_nodes()

    statistify = lambda item: (item, item.get_total_commitment(**filters))
    tot_order = lambda item: item[1]

    activities = projects_models.Activity.objects.all()
    if len(filters.keys()):
        activities = activities.filter(**filters)

    ctx = {
        'selected_code_list': selected,
        'selected_facet': selected_facet,
        'start_year': start_year,
        'end_year': end_year,
        'sector_stats': sorted(map(statistify, sectors), key=tot_order, reverse=True),
        'channel_stats': sorted(map(statistify, channels), key=tot_order, reverse=True),
        'aid_stats': sorted(map(statistify, aids), key=tot_order, reverse=True),
        'projects_count': activities.distinct('project').count(),
        'commitments_sum': activities.aggregate(Sum('commitment'))['commitment__sum'],
        'disbursements_sum': activities.aggregate(Sum('disbursement'))['disbursement__sum'],
        'years': range(start_year, end_year + 1),
        }

    return ctx