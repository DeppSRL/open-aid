from django.db.models import Min, Max, Sum
from django.views.generic import TemplateView
from django.conf import settings
from .crs import models

class Home(TemplateView):
    template_name = 'home.html'

class Numbers(Home):
    template_name = 'pages/numbers.html'
