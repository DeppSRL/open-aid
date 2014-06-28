from django.views.generic import TemplateView
from blog.models import Entry


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {
            'entries_list': Entry.objects.all().order_by('-published_at')[:3]
        }

class Numbers(Home):
    template_name = 'pages/numbers.html'
