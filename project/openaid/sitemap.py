__author__ = 'stefano'
from django.contrib.sitemaps import Sitemap, GenericSitemap
from django.core.urlresolvers import reverse
from projects.models import Initiative, Project
from codelists.models import Recipient, Sector, Agency, AidType


class BaseOpenaidSitema(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    destination_view = None
    urlconf = None
    prefix = None

    def generate_items(self):
        pass

    def location(self, item):
        return reverse(self.destination_view, urlconf=self.urlconf, prefix=self.prefix, kwargs=item)

    def items(self):
        return self.generate_items()


class InitiativeSitemap(BaseOpenaidSitema):
    destination_view = 'initiative-detail'
    urlconf = 'openaid.projects.urls'
    prefix = '/projects/'

    def generate_items(self):
        return Initiative.objects.all().order_by('code').values('code')


class ProjectSitemap(BaseOpenaidSitema):
    urlconf = 'openaid.projects.urls'
    destination_view = 'project-detail'
    prefix = '/projects/'

    def generate_items(self):
        return Project.objects.all().order_by('pk').values('pk')


class RecipientSitemap(BaseOpenaidSitema):
    urlconf = 'openaid.codelists.urls'
    destination_view = 'recipient-detail'
    prefix = '/code-lists/'

    def generate_items(self):
        return Recipient.objects.all().order_by('code').values('code')


class AgencySitemap(BaseOpenaidSitema):
    urlconf = 'openaid.codelists.urls'
    destination_view = 'agency-detail'
    prefix = '/code-lists/'

    def generate_items(self):
        return Agency.objects.all().order_by('code').values('code')


class AidTypeSitemap(BaseOpenaidSitema):
    urlconf = 'openaid.codelists.urls'
    destination_view = 'aid_type-detail'
    prefix = '/code-lists/'

    def generate_items(self):
        return AidType.objects.all().order_by('code').values('code')


sitemaps = {
    'initiatives': InitiativeSitemap,
    'projects': ProjectSitemap,
    'recipients': RecipientSitemap,
    'agencies': AgencySitemap,
    'aid-type': AidTypeSitemap,
}