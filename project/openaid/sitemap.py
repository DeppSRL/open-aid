__author__ = 'stefano'
from django.contrib.sitemaps import Sitemap, GenericSitemap
from django.core.urlresolvers import reverse
from django.conf import settings
from projects.models import Initiative, Project

class BaseOpenaidSitema(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def location(self, item):
        return reverse(self.destination_view, urlconf='openaid.projects.urls', kwargs=item)

    def items(self):
        return self.generate_items()

class InitiativeSitemap(BaseOpenaidSitema):

    destination_view = 'initiative-detail'

    def generate_items(self):
        return Initiative.objects.all().order_by('code').values('code')




class ProjectSitemap(BaseOpenaidSitema):
    destination_view = 'project-detail'

    def generate_items(self):
        return Project.objects.all().order_by('pk').values('pk')


sitemaps = {

    'initiatives': InitiativeSitemap,
    'projects': ProjectSitemap,
    }