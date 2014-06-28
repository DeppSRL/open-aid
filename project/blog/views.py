from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Entry
from tagging.views import TagFilterMixin
from openaid.mixins import DateFilterMixin

class BlogView(ListView, TagFilterMixin, DateFilterMixin):
    model = Entry
    template_name = "entry_list.html"

    def get_queryset(self):
        queryset = super(BlogView, self).get_queryset()
        queryset = self._apply_date_filter(queryset)
        queryset = self._apply_tag_filter(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context['date_choices'] = self._get_date_choices()
        context['tag_choices'] = self._get_tag_choices()

        return context

class BlogEntryView(DetailView):
    model = Entry
    template_name = "entry_detail.html"

def blogEntryItem(request, slug):
    entry = get_object_or_404(Entry, slug=slug)
    return render_to_response('entry_item.html', {'full_view': 1, 'title_linked': 1, 'object': entry})
