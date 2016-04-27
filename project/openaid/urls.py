# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from . import views

# load admin modules
from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^$', views.Home.as_view()),
    url(r'^widget/$', views.Widget.as_view(), name='widget'),
    url(r'^widget/embed/$', views.WidgetEmbed.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

openaid_urls = (
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^news/', include('blog.urls')),
    url(r'^faq/', include('faq.urls')),
    url(r'^projects/', include('openaid.projects.urls', namespace='projects')),
    url(r'^code-lists/', include('openaid.codelists.urls', namespace='codelists')),
    url(r'^', include('openaid.pages.urls')),
)
urlpatterns += i18n_patterns('', *openaid_urls)

# static and media urls not works with DEBUG = True, see static function.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('', url(r'^__debug__/', include(debug_toolbar.urls)), )
