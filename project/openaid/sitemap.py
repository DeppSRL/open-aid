__author__ = 'stefano'
from django.contrib.sitemaps import Sitemap, GenericSitemap
from django.core.urlresolvers import reverse
from django.conf import settings
from projects.models import Initiative

class InitiativeSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    destination_view = 'initiative-detail'

    """Reverse static views for XML sitemap."""

    def generate_items(self):

        excluded_sectors = settings.OPENAID_INITIATIVE_PURPOSE_EXCLUDED
        return Initiative.objects.all().exclude(purpose_temp__code__in=excluded_sectors).order_by('code').values('code')

    def location(self, item):

        return reverse(self.destination_view, urlconf='openaid.projects.urls', kwargs=item)

    def items(self):

        return self.generate_items()



sitemaps = {

    'initiatives': InitiativeSitemap,
    }