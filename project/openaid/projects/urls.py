# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from haystack.views import search_view_factory
from . import views

# load admin modules
from django.contrib import admin
admin.autodiscover()


urls = (
    url(r'^project/list/$', views.ProjectList.as_view(), name='project-list'),
    url(r'^project/(?P<pk>\d+)/$', views.ProjectDetail.as_view(), name='project-detail'),
    url(r'^activity/list/$', views.ActivityList.as_view(), name='activity-list'),
    url(r'^activity/(?P<pk>\d+)/$', views.ActivityDetail.as_view(), name='activity-detail'),

    url(r'^search/', search_view_factory(
        views.SearchFacetedProjectView, facets=[
            'years', 'recipients', 'agencies', 'aid_types', 'channels',
            'finance_types', 'sectors']
    ), name='search'),
)
urlpatterns = patterns('', *urls)
