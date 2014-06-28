from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home.html'

class Numbers(Home):
    template_name = 'pages/numbers.html'
