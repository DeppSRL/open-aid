from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'^$', BlogView.as_view(), name='blog_home'),
    url(r'^/articolo/(?P<slug>[\w-]+)$', BlogEntryView.as_view(), name='blog_item'),
    url(r'^/load/(?P<slug>[\w-]+)$', blogEntryItem, name='blog_item_load'),
)