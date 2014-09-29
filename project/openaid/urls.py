# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.views import APIView
from .projects.views import ProjectViewSet, ActivityViewSet, ChannelReportedViewSet
from .codelists.views import SectorViewSet, RecipientViewSet, ChannelViewSet, AidTypeViewSet, AgencyViewSet, \
    FinanceTypeViewSet, DonorViewSet

# load admin modules
from django.contrib import admin
admin.autodiscover()


# Create a router and register our viewsets with it.
class APIRouter(DefaultRouter):

    def get_api_root_view(self):
        """
        Return a view to use as the API root.
        """
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        class APIRoot(APIView):
            """
            This is the root entry-point of the OpenAID APIs.

            The APIs are read-only, freely accessible to all through HTTP requests at ``http://openaid.esteri.it/api``.

            Responses are emitted in both **browseable-HTML** and **JSON** formats (``http://openaid.esteri.it/api/.json``)

            To serve all requests and avoid slow responses or downtimes due to misuse, we limit the requests rate.
            When accessing the API **anonymously**, your client is limited to **12 requests per minute** from the same IP.
            You can contact us to become an **authenticated API user** (it's still free),
            then the rate-limit would be lifted to **1 request per second**.

            If for some reasons, you need to scrape all the OpenAID data, please consider a bulk **CSV download**.
            
            See the ``http://openaid.esteri.it/scarica-dati/`` page in the web site.
            """
            _ignore_model_permissions = True

            def get(self, request, format=None):
                ret = {}
                for key, url_name in api_root_dict.items():
                    ret[key] = reverse(url_name, request=request, format=format)
                return Response(ret)

        return APIRoot.as_view()

router = APIRouter(trailing_slash=False)
router.register(r'projects', ProjectViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'sectors', SectorViewSet)
router.register(r'recipients', RecipientViewSet)
router.register(r'channels', ChannelViewSet)
router.register(r'aid_types', AidTypeViewSet)
router.register(r'agencies', AgencyViewSet)
router.register(r'finance_types', FinanceTypeViewSet)
# router.register(r'donors', DonorViewSet)
router.register(r'channel_reported', ChannelReportedViewSet)


urlpatterns = [
    url(r'^$', views.Home.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
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
