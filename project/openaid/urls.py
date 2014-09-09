# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework.routers import DefaultRouter
from . import views
from .projects.views import ProjectViewSet, ActivityViewSet
from .codelists.views import SectorViewSet, RecipientViewSet, ChannelViewSet, AidTypeViewSet, AgencyViewSet, \
    FinanceTypeViewSet, DonorViewSet

# load admin modules
from django.contrib import admin
admin.autodiscover()


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'sectors', SectorViewSet)
router.register(r'recipients', RecipientViewSet)
router.register(r'channels', ChannelViewSet)
router.register(r'aid_types', AidTypeViewSet)
router.register(r'agencies', AgencyViewSet)
router.register(r'finance_types', FinanceTypeViewSet)
router.register(r'donors', DonorViewSet)


urlpatterns = [
    url(r'^$', views.Home.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^api/', include(router.urls)),
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
