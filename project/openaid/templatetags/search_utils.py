from django import template
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.utils.http import urlquote, urlencode

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
    url = reverse('projects:search')

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
        query = QueryDict('', mutable=True)
        query.update({
            'selected_facets': value
        })
        return u"{0}?{1}".format(url, query.urlencode(safe=':/'))

    query = context['request'].GET.copy()
    if remove:
        if value in query.getlist('selected_facets'):
            query.setlist('selected_facets', filter(
                lambda x: x != value, query.getlist('selected_facets')
            ))
    else:
        if value not in query.getlist('selected_facets'):
            query.appendlist('selected_facets', value)

    # remove page from query to avoid empty pages
    if 'page' in query:
        del query['page']
        
    return u"{0}?{1}".format(url, query.urlencode(safe=':/'))


@register.inclusion_tag('search/facet_filters.html', takes_context=True)
def show_facets(context, facet, skip_empty=True, multi_select=False, codelist=None):
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
    codelist_terms = []
    for term, count in context['facets']['fields'][facet]:

        if skip_empty and count == 0:
            continue

        is_term_selected = u'{0}:{1}'.format(facet, term) in selected_facets

        if is_term_selected:

            if not multi_select and len(result_context['selected_terms']) > 0:
                raise template.TemplateSyntaxError(u"Cannot render multi selectable facets. "
                                                   u"Add multi_select option".format(facet))
            result_context['selected_terms'].append(term)

        if codelist:
            codelist_terms.append(term)

        result_context['terms'].append({
            'term': term,
            'count': count,
            'is_selected': is_term_selected,
            'label': term,
        })

    if result_context['selected_terms'] and not multi_select and result_context['terms']:
        # if not multi_select mode, after a term selection
        # user see only the remove link for selected term
        result_context['terms'] = filter(
            lambda T: T['term'] in result_context['selected_terms'],
            result_context['terms']
        )

    if codelist and len(codelist_terms) > 0:
        # take labels localized from database
        from ..codelists import models
        terms = dict(models.get_codelist(codelist).objects.filter(code__in=codelist_terms).values_list('code', 'name'))
        for item in result_context['terms']:
            item['label'] = terms[item['term']]

    return result_context