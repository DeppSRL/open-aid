# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from haystack.views import search_view_factory
from . import views


urls = (
    url(r'^initiative/(?P<code>\d+)/$', views.InitiativeDetail.as_view(), name='initiative-detail'),
    url(r'^project/list/$', views.ProjectList.as_view(), name='project-list'),
    url(r'^project/(?P<pk>\d+)/$', views.ProjectDetail.as_view(), name='project-detail'),
    # NOTE: search/ is here for back-compatibility
    url(r'^search/', search_view_factory(views.SearchFacetedProjectView), name='search'),
    url(r'project/search/', search_view_factory(views.SearchFacetedProjectView), name='project-search'),
    url(r'initiative/search/', search_view_factory(views.SearchFacetedInitiativeView), name='initiative-search'),

)
urlpatterns = patterns('', *urls)
