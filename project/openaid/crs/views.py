from django.views.generic import DetailView, ListView, TemplateView
from django.db.models import Count, Max, Min, Sum
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView
from . import models
from .forms import FacetedActivitySearchForm


class CodeListView(object):
    slug_field = 'code'
    slug_url_kwarg = 'code'


class SectorView(CodeListView, DetailView):
    model = models.Sector


class RecipientView(CodeListView, DetailView):
    model = models.Recipient


class ChannelView(CodeListView, DetailView):
    model = models.Channel


class AidTypeView(CodeListView, DetailView):
    model = models.AidType



class ProjectDetail(DetailView):
    model = models.Project

class ProjectList(ListView):
    model = models.Project
    paginate_by = 50

    def get_queryset(self):

        order_by = self.request.GET.get('order_by', None)
        # add `activities_count` field to project
        queryset = super(ProjectList, self).get_queryset().annotate(
            activities_count=Count('activity')
        )

        for valid_filter in ('recipient', 'crs'):
            if valid_filter in self.request.GET:
                queryset = queryset.filter(**{
                    valid_filter: self.request.GET.get(valid_filter)
                })

        if order_by:
            direction = ''
            if order_by.startswith('-'):
                direction, order_by = order_by[0], order_by[1:]
            if order_by in ('activities', 'crs', 'recipient'):
                if order_by == 'activities':
                    return queryset.order_by('{0}activities_count'.format(direction))
                queryset = queryset.order_by("{0}{1}".format(direction, order_by))
        return queryset
class ActivityDetail(DetailView):
    model = models.Activity

class ActivityList(ListView):
    model = models.Activity
    paginate_by = 50

class ProjectActivityList(ActivityList):

    def get_queryset(self):
        project_pk = self.kwargs.get('pk')
        return super(ProjectActivityList, self).get_queryset().filter(project=int(project_pk))


class SearchFacetedActivityView(FacetedSearchView):

    template = 'crs/activity_search_results.html'

    def __init__(self, *args, **kwargs):

        sqs = SearchQuerySet()

        for facet in kwargs.pop('facets', []):
            sqs = sqs.facet(facet)

        super(SearchFacetedActivityView, self).__init__(
            form_class=FacetedActivitySearchForm, searchqueryset=sqs, *args, **kwargs)

    def extra_context(self):
        """
        Builds extra context, to build facets filters and breadcrumbs
        """
        extra = super(SearchFacetedActivityView, self).extra_context()
        extra['n_results'] = len(self.results)

        # make get array as mutable QueryDict
        params = self.request.GET.copy()
        if 'q' not in params:
            params.update({'q': ''})
        if 'page' in params:
            params.pop('page')
        extra['params'] = params

        if not self.results:
            extra['facets'] = self.form.search().facet_counts()
        else:
            extra['facets'] = self.results.facet_counts()

        extra['order_by'] = self.request.GET.get('order_by', self.form.default_order)

        return extra