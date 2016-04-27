from __future__ import print_function
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

        focus = Project.get_top_projects(year=self.request.GET.get('year', contexts.END_YEAR), qnt=1, project__has_focus=True)
        top_projects = Project.get_top_projects(qnt=3 if len(focus) else 4, year=self.request.GET.get('year', contexts.END_YEAR))

        # se non ci sono focus, prendo uno dei progetti piu importanti.
        if not len(focus) and top_projects:
            focus = top_projects[0]
            top_projects = top_projects[1:]
        else:
            focus = focus[0]

        return super(Home, self).get_context_data(
            project_focus=focus,
            entries_list=Entry.objects.all().order_by('-published_at')[:1],
            top_projects=top_projects,
            **kwargs
        )

class Numbers(Home):
    template_name = 'pages/numbers.html'


class Widget(Home):
    template_name = 'widget.html'

    def get_context_data(self, **kwargs):
        return super(Widget, self).get_context_data(widget=True, **kwargs)


class WidgetEmbed(TemplateView):
    template_name = 'widget_embed.html'

    def get_context_data(self, **kwargs):
        from django.core.urlresolvers import reverse
        from django.contrib.staticfiles.templatetags.staticfiles import static
        url = self.request.build_absolute_uri(reverse('widget'))
        js_url = self.request.build_absolute_uri(static('js/widget.js'))

        return super(WidgetEmbed, self).get_context_data(widget_url=url,js_url=js_url, **kwargs)
