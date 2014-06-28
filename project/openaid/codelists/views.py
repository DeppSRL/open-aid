from django.views.generic import DetailView
from . import models


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

