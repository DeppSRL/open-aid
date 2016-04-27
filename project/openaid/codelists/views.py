from django.views.generic import DetailView
from django.conf import settings
from . import models
from .. import views
from .. import contexts
from openaid.codelists import serializers
from openaid.views import OpenaidViewSet
from openaid import utils

class CodeListView(views.MapFiltersContextMixin, DetailView):
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_codelist_filter(self):
        if not hasattr(self, '_codelist_filter'):
            setattr(self, '_codelist_filter', {
                '%s__in' % self.model.code_list: self.object.get_descendants_pks(include_self=True)
            })
        return getattr(self, '_codelist_filter')

    def get_context_data(self, **kwargs):
        context = super(CodeListView, self).get_context_data(**kwargs)
        context = DetailView.get_context_data(self, **context)

        # adds model name to the context so the app knows which page of codelist it's rendering
        model_name = self.model.__name__.lower()
        context.update({'model_name': model_name})

        year_value = utils.sanitize_get_param(int,self.request.GET.get('year'),contexts.END_YEAR,top=contexts.END_YEAR,length=4)
        # depending on which codelist page it's rendereing adds top projs or top inits
        if model_name in ['agency', 'aidtype']:
            context['top_projects'] = self.object.top_projects(year=year_value)
        elif model_name in ['recipient', 'sector']:
            top_initiatives = self.object.top_initiatives()
            context['top_initiatives'] = top_initiatives[:settings.TOP_ELEMENTS_NUMBER]
            context['top_initiatives_count'] = len(top_initiatives)

        return context

    def get_map_filters(self):
        filters = super(CodeListView, self).get_map_filters()
        filters.update(self.get_codelist_filter())
        return filters


class SectorView(CodeListView):
    model = models.Sector


class RecipientView(CodeListView):
    model = models.Recipient


class ChannelView(CodeListView):
    model = models.Channel


class AidTypeView(CodeListView):
    model = models.AidType


class AgencyView(CodeListView):
    model = models.Agency


class CodelistOpenaidViewSet(OpenaidViewSet):
    lookup_field = 'code'


class SectorViewSet(CodelistOpenaidViewSet):
    queryset = models.Sector.objects.all()
    serializer_class = serializers.SectorSerializer


class RecipientViewSet(CodelistOpenaidViewSet):
    queryset = models.Recipient.objects.all()
    serializer_class = serializers.RecipientSerializer


class ChannelViewSet(CodelistOpenaidViewSet):
    queryset = models.Channel.objects.all()
    serializer_class = serializers.ChannelSerializer


class AidTypeViewSet(CodelistOpenaidViewSet):
    queryset = models.AidType.objects.all()
    serializer_class = serializers.AidTypeSerializer


class AgencyViewSet(CodelistOpenaidViewSet):
    queryset = models.Agency.objects.all()
    serializer_class = serializers.AgencySerializer


class FinanceTypeViewSet(CodelistOpenaidViewSet):
    queryset = models.FinanceType.objects.all()
    serializer_class = serializers.FinanceTypeSerializer


class DonorViewSet(CodelistOpenaidViewSet):
    queryset = models.Donor.objects.all()
    serializer_class = serializers.DonorSerializer
