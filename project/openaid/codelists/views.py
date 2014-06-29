from django.views.generic import DetailView, View
from . import models


class CodeListView(DetailView):
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_context_data(self, **kwargs):
        return super(CodeListView, self).get_context_data(
            map_values=models.Recipient.get_map_totals(**self.get_map_filters()),
            **kwargs)

    def get_map_filters(self):
        return {
            '%s__in' % self.model.code_list: self.get_object().get_descendants_pks(include_self=True)
        }

class SectorView(CodeListView, DetailView):
    model = models.Sector


class RecipientView(CodeListView, DetailView):
    model = models.Recipient

    def get_context_data(self, **kwargs):
        # bypass totale_territori loader
        return DetailView.get_context_data(self, **kwargs)


class ChannelView(CodeListView, DetailView):
    model = models.Channel


class AidTypeView(CodeListView, DetailView):
    model = models.AidType

