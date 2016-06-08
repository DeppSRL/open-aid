from django.views.generic import DetailView, ListView, TemplateView
from django.db.models import Count, Sum
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView
from . import models
from .forms import FacetedProjectSearchForm, FacetedInitiativeSearchForm
from openaid.views import OpenaidViewSet
from .serializers import ProjectSerializer, ProjectDetailSerializer, ActivitySerializer, ChannelReportedSerializer


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


class ActivityList(ListView):
    model = models.Activity
    paginate_by = 50


class SearchFacetedAbstractView(FacetedSearchView):

    facets = []

    def __init__(self, *args, **kwargs):

        sqs = SearchQuerySet(using=self.using).order_by('-end_year')

        for facet in self.facets:
            sqs = sqs.facet(facet, mincount=1, limit=300)

        super(SearchFacetedAbstractView, self).__init__(
            form_class=FacetedProjectSearchForm, searchqueryset=sqs, *args, **kwargs)

    def extra_context(self):
        """
        Builds extra context, to build facets filters and breadcrumbs
        """
        extra = super(SearchFacetedAbstractView, self).extra_context()
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


class SearchFacetedProjectView(SearchFacetedAbstractView):
    using = 'default'
    form_class = FacetedProjectSearchForm
    template = 'search/project_search_results.html'
    facets = [
        'years', 'recipient', 'agencies', 'aid_types', 'channels',
        'finance_types', 'sectors'
    ]


class SearchFacetedInitiativeView(SearchFacetedAbstractView):
    using = 'initiatives'
    form_class = FacetedInitiativeSearchForm
    template = 'search/initiative_search_results.html'
    facets = [
        'years', 'recipients', 'agency', 'aid_types', 'channels',
        'finance_type', 'sectors'
    ]


class ProjectViewSet(OpenaidViewSet):
    """
    List of all **projects**.

    A Project contains a list of **Activities**.

    Projects can be filtered through filters below in the GET query-string parameters:

    * ``crsid``
    * ``start_year``
    * ``end_year``
    * ``recipient``
    * ``channel``
    * ``aid_type``
    * ``agency``
    * ``finance_type``
    * ``sector``

    Filters use codes, and multiple filters can be built.

    Codes values to be used in the filters are shown in the project list, and the complete lists can be extracted at:

    * ``/api/recipient``
    * ``/api/channel``
    * ``/api/aid_type``
    * ``/api/agency``
    * ``/api/finance_type``
    * ``/api/sector``

    Examples
    ========

    * ``/api/projects?recipient=298``
    * ``/api/projects?start_year=2004``

    The results are paginated by default to 25 items per page.
    The number of items per page can be changed through the ``page_size`` GET parameter.

    Results are sorted by default by descending year (``-year``).
    You can change the sorting order, using the ``ordering`` GET parameter.
    These are the possible values:

    * ``start_year``
    * ``end_year``

    a minus (-) in front of the field name indicates a *descending* order criterion.
    """

    queryset = models.Project.objects.all().prefetch_related('activity_set').select_related(
        'channel', 'aid_type', 'agency', 'finance_type', 'sector', 'markers'
    )
    serializer_class = ProjectSerializer
    filter_fields = ('crsid', 'start_year', 'end_year', )
    ordering_fields = (
        'start_year',
        'end_year',
    )

    def get_queryset(self):
        queryset = self.queryset

        for codelist in (
            'recipient',
            'channel',
            'aid_type',
            'agency',
            'finance_type',
            'sector',
        ):
            codelist_code = self.request.QUERY_PARAMS.get(codelist, None)
            if codelist_code:
                queryset = queryset.filter(**{
                    "%s__code" % codelist: codelist_code
                })

        return queryset

    def get_serializer_class(self):
        if getattr(self, 'object', False):
            return ProjectDetailSerializer
        return super(ProjectViewSet, self).get_serializer_class()


class ActivityViewSet(OpenaidViewSet):
    """
    List of all **activities**.

    Activities can be filtered through filters below in the GET query-string parameters:

    ``crsid`` ``year`` ``title`` ``description`` ``recipient`` ``channel`` ``aid_type`` ``agency`` ``finance_type``
    ``sector`` ``channel_reported`` ``geography`` ``report_type`` ``flow_type`` ``bi_multi`` ``is_ftc`` ``is_pba``
    ``is_investment`` ``grant_element`` ``number_repayment`` ``expected_start_date`` ``completion_date`` ``commitment_date``.

    Filters use codes, and multiple filters can be built.

    Codes values to be used in the filters are shown in the activity list, and the complete lists can be extracted at:

    * ``/api/recipient``
    * ``/api/channel``
    * ``/api/aid_type``
    * ``/api/agency``
    * ``/api/finance_type``
    * ``/api/sector``

    Examples
    ========

    * ``/api/activities?recipient=298``
    * ``/api/activities?channel=istruzione``
    * ``/api/activities?year=2004``
    * ``/api/activities?is_ftc=true``
    * ``/api/activities?recipient=298&channel=10000``

    The results are paginated by default to 25 items per page.
    The number of items per page can be changed through the ``page_size`` GET parameter.

    Results are sorted by default by descending year (``-year``).
    You can change the sorting order, using the ``ordering`` GET parameter.
    These are the possible values:

    * ``commitment``
    * ``commitment_usd``
    * ``disbursement``
    * ``disbursement_usd``
    * ``expected_start_date``
    * ``completion_date``
    * ``commitment_date``

    a minus (-) in front of the field name indicates a *descending* order criterion.

    """

    queryset = models.Activity.objects.all().select_related(
        'project',
        'markers',
        'recipient',
        'channel',
        'aid_type',
        'agency',
        'finance_type',
        'sector',
        'channel_reported',
    )
    filter_fields = (
        'crsid',
        'year',
        'title',
        'description',
        'channel_reported',

        'geography',
        'report_type',
        'flow_type',
        'bi_multi',
        'is_ftc',
        'is_pba',
        'is_investment',

        'commitment',
        'commitment_usd',
        'disbursement',
        'disbursement_usd',
        'grant_element',
        'number_repayment',
        'expected_start_date',
        'completion_date',
        'commitment_date',

    )
    serializer_class = ActivitySerializer
    ordering_fields = (
        'year',
        'commitment',
        'commitment_usd',
        'disbursement',
        'disbursement_usd',
        'expected_start_date',
        'completion_date',
        'commitment_date',
    )

    def get_queryset(self):
        queryset = self.queryset

        for codelist in (
            'recipient',
            'channel',
            'aid_type',
            'agency',
            'finance_type',
            'sector',
        ):
            codelist_code = self.request.QUERY_PARAMS.get(codelist, None)
            if codelist_code:
                queryset = queryset.filter(**{
                    "%s__code" % codelist: codelist_code
                })

        return queryset


class ChannelReportedViewSet(OpenaidViewSet):
    queryset = models.ChannelReported.objects.all()
    serializer_class = ChannelReportedSerializer


class InitiativeDetail(DetailView):
    model = models.Initiative
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_context_data(self, **kwargs):
        obj = self.object
        projects = obj.project_set.annotate(
            total_commitment=Sum('activity__commitment'),
            total_disbursement=Sum('activity__disbursement')
        )
        obj.total_disbursement = obj.total_commitment = 0.0
        for p in projects:
            if p.total_commitment:
                obj.total_commitment += p.total_commitment
            if p.total_disbursement:
                obj.total_disbursement += p.total_disbursement

        # aggregate to the obj the docs and the photos
        obj.documents = obj.document_set.all()
        obj.photos = obj.photo_set.all()

        return super(InitiativeDetail, self).get_context_data(
            projects=projects,
            **kwargs)
