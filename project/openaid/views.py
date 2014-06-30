from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from blog.models import Entry
from openaid import contexts
from openaid.codelists.models import Recipient
from openaid.projects.models import Project


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
        return super(Home, self).get_context_data(
            entries_list=Entry.objects.all().order_by('-published_at')[:3],
            top_projects=Project.get_top_projects(year=self.request.GET.get('year', contexts.END_YEAR)),
            **kwargs
        )

class Numbers(Home):
    template_name = 'pages/numbers.html'
