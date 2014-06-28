from django.db.models import Min, Max, Sum
from django.views.generic import TemplateView
from django.conf import settings
from blog.models import Entry
from .crs import models

class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {
            'entries_list': Entry.objects.all().order_by('-published_at')[:3]
        }

class Numbers(Home):
    template_name = 'pages/numbers.html'
