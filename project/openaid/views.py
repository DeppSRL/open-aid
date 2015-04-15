from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from rest_framework import viewsets
from blog.models import Entry
from openaid import contexts
from openaid.codelists.models import Recipient
from openaid.projects.models import Project, Initiative


class MapFiltersContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        return super(MapFiltersContextMixin, self).get_context_data(
            map_values=Recipient.get_map_totals(**self.get_map_filters()),
            **kwargs)

    def get_map_filters(self):
        # the exact lookup is necessary becouse year is already a lookup
        return {'year__exact': self.request.GET.get('year', contexts.END_YEAR)}


class Home(MapFiltersContextMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):

        top_initiatives = Initiative.get_top_initiatives(6, year=self.request.GET.get('year', contexts.END_YEAR))

        # focus = Project.get_top_projects(year=self.request.GET.get('year', contexts.END_YEAR), qnt=1, project__has_focus=True)
        # top_projects = Project.get_top_projects(qnt=3 if len(focus) else 4, year=self.request.GET.get('year', contexts.END_YEAR))

        # se non ci sono focus, prendo uno dei progetti piu importanti.
        # if not len(focus) and top_projects:
        #     focus = top_projects[0]
        #     top_projects = top_projects[1:]
        # else:
        #     focus = focus[0]

        return super(Home, self).get_context_data(
            # project_focus=focus,
            entries_list=Entry.objects.all().order_by('-published_at')[:1],
            # top_projects=top_projects,
            top_initiatives=top_initiatives,
            **kwargs
        )

class Numbers(Home):
    template_name = 'pages/numbers.html'


class OpenaidViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100


from rest_framework import generics

class OpenaidApiRoot(generics.GenericAPIView):
    """
    This is the root entry-point of the OpenCoesione APIs.

    The APIs are read-only, freely accessible to all through HTTP requests at ``http://www.opencoesione.gov/api``.

    Responses are emitted in both **browseable-HTML** and **JSON** formats (``http://www.opencoesione.gov/api/.json``)

    To serve all requests and avoid slow responses or downtimes due to misuse, we limit the requests rate.
    When accessing the API **anonymously**, your client is limited to **12 requests per minute** from the same IP.
    You can contact us to become an **authenticated API user** (it's still free),
    then the rate-limit would be lifted to **1 request per second**.

    Authentication is done through HTTP Basic Authentication.

    You can request a username/password to authenticate,
    by writing an email to the following address: opencoesione@dps.gov.it.

    If for some reasons, you need to scrape all the OpenCoesione data, please consider a bulk **CSV download**.
    See the ``http://www.opencoesione.gov.it/opendata/`` page in the web site.
    """