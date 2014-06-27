from django import template
from django.core.urlresolvers import reverse
register = template.Library()


@register.simple_tag(takes_context=True)
def search_url_page(context, page):
    """
    This is a shortcut to create a search results page link.
    """
    url = context['request'].path
    q = context['request'].GET.copy()
    q['page'] = int(page)
    return u"{0}?{1}".format(url, q.urlencode(safe=':/'))


@register.simple_tag(takes_context=True)
def search_url_order(context, order):
    """
    This is a shortcut to create a search results page link.
    """
    url = context['request'].path
    q = context['request'].GET.copy()
    q['order_by'] = order
    q['desc'] = 1
    return u"{0}?{1}".format(url, q.urlencode(safe=':/'))



@register.simple_tag(takes_context=True)
def search_url(context, facet='', term='', remove=False, absolute=True):
    """
    Generate search url starting from action-list defined url.
    If absolute is True (as default) this tag remove all other facets,
    to returns only the provided one (facet:term).
    Else replace or append provided facet:term.
    If remove is True this tag remove only provided facet:term.
    """
    url = reverse('crs:activity-search')

    if not facet:
        return url

    if not term:
        if absolute:
            return u"{0}?q={1}".format(url, facet)
        else:
            query = context['request'].GET.copy()
            query['q'] = facet
            return u"{0}?{1}".format(url, query.urlencode(safe=':/'))

    value = u"{0}:{1}".format(facet, term)

    if absolute:
        return u"{0}?selected_facets={1}".format(url, value)

    query = context['request'].GET.copy()
    if remove:
        if value in query.getlist('selected_facets'):
            query.setlist('selected_facets', filter(
                lambda x: x != value, query.getlist('selected_facets')
            ))
    else:
        if value not in query.getlist('selected_facets'):
            query.appendlist('selected_facets', value)

    return u"{0}?{1}".format(url, query.urlencode(safe=':/'))


@register.inclusion_tag('crs/facet_filters.html', takes_context=True)
def show_facets(context, facet, skip_empty=True, multi_select=False):
    """
This inclusion tag prints a list of facet terms.
"""
    if ('facets' not in context) or ('fields' not in context['facets']) or (facet not in context['facets']['fields']):
        raise template.TemplateSyntaxError(u"Cannot retrieve facet '{0}' from context facets fields".format(facet))

    selected_facets = context['request'].GET.getlist('selected_facets', [])
    result_context = {
        'facet': facet,
        'request': context['request'],
        'terms': [],
        'selected_terms': [],
        'multi_select': multi_select,
    }

    for term, count in context['facets']['fields'][facet]:

        if skip_empty and count == 0:
            continue

        is_term_selected = u'{0}:{1}'.format(facet, term) in selected_facets

        if is_term_selected:

            if not multi_select and len(result_context['selected_terms']) > 0:
                raise template.TemplateSyntaxError(u"Cannot render multi selectable facets. "
                                                   u"Add multi_select option".format(facet))
            result_context['selected_terms'].append(term)

        result_context['terms'].append({
            'term': term,
            'count': count,
            'is_selected': is_term_selected,
        })

    if result_context['selected_terms'] and not multi_select and result_context['terms']:
        # if not multi_select mode, after a term selection
        # user see only the remove link for selected term
        result_context['terms'] = filter(
            lambda T: T['term'] in result_context['selected_terms'],
            result_context['terms']
        )

    return result_context