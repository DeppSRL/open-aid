# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from . import views

# load admin modules
from django.contrib import admin
admin.autodiscover()


urls = (
    url(r'^project/list/$', views.ProjectList.as_view(), name='project-list'),
    url(r'^project/(?P<pk>\d+)/$', views.ProjectDetail.as_view(), name='project-detail'),
    url(r'^activity/list/$', views.ActivityList.as_view(), name='activity-list'),
    url(r'^activity/(?P<pk>\d+)/$', views.ActivityDetail.as_view(), name='activity-detail'),

    url(r'^sectors/(?P<code>\w+)/$', views.SectorView.as_view(), name='sector-detail'),
    url(r'^recipients/(?P<code>\w+)/$', views.RecipientView.as_view(), name='recipient-detail'),
    url(r'^channels/(?P<code>\w+)/$', views.ChannelView.as_view(), name='channel-detail'),
    url(r'^aid_type/(?P<code>\w+)/$', views.AidTypeView.as_view(), name='aid_type-detail'),

)
urlpatterns = patterns('', *urls)
