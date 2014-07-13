# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from . import views

# load admin modules
from django.contrib import admin
admin.autodiscover()


urls = (
    url(r'^sectors/(?P<code>\w+)/$', views.SectorView.as_view(), name='sector-detail'),
    url(r'^recipients/(?P<code>\w+)/$', views.RecipientView.as_view(), name='recipient-detail'),
    url(r'^channels/(?P<code>\w+)/$', views.ChannelView.as_view(), name='channel-detail'),
    url(r'^agencies/(?P<code>\w+)/$', views.AgencyView.as_view(), name='agency-detail'),
    url(r'^aid_types/(?P<code>\w+)/$', views.AidTypeView.as_view(), name='aid_type-detail'),
    url(r'^finance_types/(?P<code>\w+)/$', views.FinanceTypeView.as_view(), name='finance_type-detail'),
    url(r'^donors/(?P<code>\w+)/$', views.DonorView.as_view(), name='donor-detail'),
)
urlpatterns = patterns('', *urls)
