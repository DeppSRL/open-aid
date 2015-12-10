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
    url(r'^agencies/(?P<code>\w+)/$', views.AgencyView.as_view(), name='agency-detail'),
    url(r'^aid_types/(?P<code>\w+)/$', views.AidTypeView.as_view(), name='aid_type-detail'),
)
urlpatterns = patterns('', *urls)
