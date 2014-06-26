from __future__ import absolute_import
from django import template
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Min, Max, Sum
from .. import models
from ... import contexts
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter(is_safe=True)
def currency(amount):
    return intcomma(floatformat((amount or 0.0) * settings.OPENAID_MULTIPLIER, 0))


@register.inclusion_tag('commons/stats.html', takes_context=True)
def crs_stats(context, recipient=None, **kwargs):

    start_year = contexts.START_YEAR
    end_year = contexts.END_YEAR
    selected_year = context.get(contexts.YEAR_FIELD, None) or end_year

    filters = {
        'year': selected_year,
    }

    if recipient:
        filters['project__recipient'] = recipient

    sector = kwargs.get('sector', None)
    if sector:
        filters['purpose__in'] = sector.get_descendants_pks(include_self=True)

    channel = kwargs.get('channel', None)
    if channel:
        filters['channel__in'] = channel.get_descendants_pks(include_self=True)

    aid = kwargs.get('aid', None)
    if aid:
        filters['aid_type__in'] = aid.get_descendants_pks(include_self=True)

    sectors = sector.children.all() if sector else models.Sector.objects.get(parent__isnull=True).children.all()
    channels = channel.children.all() if channel else models.Channel.objects.filter(parent__isnull=True)
    aids = aid.children.all() if aid else models.AidType.objects.get(parent__isnull=True).children.all()

    statistify = lambda item: (item, item.get_total_commitment(**filters))

    activities = models.Activity.objects.all()
    if len(filters.keys()):
        activities = activities.filter(**filters)

    ctx = {
        'start_year': start_year,
        'end_year': end_year,
        'sector_stats': map(statistify, sectors),
        'channel_stats': map(statistify, channels),
        'aid_stats': map(statistify, aids),
        'projects_count': activities.distinct('project').count(),
        'commitments_sum': activities.aggregate(Sum('usd_commitment'))['usd_commitment__sum'],
        'disbursements_sum': activities.aggregate(Sum('usd_disbursement'))['usd_disbursement__sum'],
        'years': range(start_year, end_year + 1),
    }

    return ctx