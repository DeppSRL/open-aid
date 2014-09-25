from django.views.generic import DetailView
from . import models
from .. import views
from .. import contexts
from openaid.codelists import serializers
from openaid.views import OpenaidViewSet


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
        context.update({
            'top_projects': self.object.top_projects(year=self.request.GET.get('year', contexts.END_YEAR))
        })
        return context

    def get_map_filters(self):
        filters = super(CodeListView, self).get_map_filters()
        filters.update(self.get_codelist_filter())
        return filters


class SectorView(CodeListView):
    model = models.Sector


class RecipientView(CodeListView):
    model = models.Recipient

    def get_context_data(self, **kwargs):
        # bypass totale_territori loader
        return DetailView.get_context_data(self, top_projects=self.object.top_projects(year=self.request.GET.get('year', contexts.END_YEAR)), **kwargs)


class ChannelView(CodeListView):
    model = models.Channel


class AidTypeView(CodeListView):
    model = models.AidType


class AgencyView(CodeListView):
    model = models.Agency


class FinanceTypeView(CodeListView):
    model = models.FinanceType


class DonorView(CodeListView):
    model = models.Donor


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
