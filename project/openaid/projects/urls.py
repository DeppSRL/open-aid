# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from haystack.views import search_view_factory
from . import views



urls = (
    url(r'^initiative/(?P<code>\d+)/$', views.InitiativeDetail.as_view(), name='initiative-detail'),
    url(r'^project/list/$', views.ProjectList.as_view(), name='project-list'),
    url(r'^project/(?P<pk>\d+)/$', views.ProjectDetail.as_view(), name='project-detail'),
    url(r'^activity/list/$', views.ActivityList.as_view(), name='activity-list'),
    url(r'^activity/(?P<pk>\d+)/$', views.ActivityDetail.as_view(), name='activity-detail'),
    url(r'^stats/$', views.ProjectStatsView.as_view(), name='projects-stats'),

    url(r'^search/', search_view_factory(
        views.SearchFacetedProjectView, facets=[
            'years', 'recipient', 'agencies', 'aid_types', 'channels',
            'finance_types', 'sectors']
    ), name='search'),
)
urlpatterns = patterns('', *urls)
