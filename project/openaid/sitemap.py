__author__ = 'stefano'
from copy import copy
from django.contrib.sitemaps import Sitemap, GenericSitemap
from django.core.urlresolvers import reverse
from projects.models import Initiative, Project
from codelists.models import Recipient, Sector, Agency, AidType


class BaseOpenaidSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    destination_view = None
    urlconf = None
    prefix = None

    def get_all_items(self):
        return []

    def generate_items(self):
        all_items = self.get_all_items()
        result = []
        # doubles the elements to produce a bilingual sitemap
        for element in all_items:
            element_en = copy(element)
            element_en['language']='en'
            result.append(element_en)
            element_it=copy(element)
            element_it['language']='it'
            result.append(element_it)
        return result

    def location(self, item):
        prefix = self.prefix.format(item['language'])
        item.pop('language',None)
        return reverse(self.destination_view, urlconf=self.urlconf, prefix=prefix, kwargs=item)

    def items(self):
        return self.generate_items()

class ProjectBaseSitemap(BaseOpenaidSitemap):
    urlconf = 'openaid.projects.urls'
    prefix = '/{}/projects/'

    pass


class InitiativeSitemap(ProjectBaseSitemap):
    destination_view = 'initiative-detail'

    def get_all_items(self):
        return Initiative.objects.all().order_by('code').values('code')


class ProjectSitemap(ProjectBaseSitemap):
    destination_view = 'project-detail'

    def get_all_items(self):
        return Project.objects.all().order_by('pk').values('pk')


class CodelistBaseSitemap(BaseOpenaidSitemap):
    urlconf = 'openaid.codelists.urls'
    prefix = '/{}/code-lists/'

    pass
  
    
class RecipientSitemap(CodelistBaseSitemap):
    destination_view = 'recipient-detail'

    def get_all_items(self):
        return Recipient.objects.all().order_by('code').values('code')


class AgencySitemap(CodelistBaseSitemap):
    destination_view = 'agency-detail'

    def get_all_items(self):
        return Agency.objects.all().order_by('code').values('code')


class AidTypeSitemap(CodelistBaseSitemap):
    destination_view = 'aid_type-detail'

    def get_all_items(self):
        return AidType.objects.root_nodes().order_by('code').values('code')


class SectorSitemap(CodelistBaseSitemap):
    destination_view = 'sector-detail'

    def get_all_items(self):
        return Sector.objects.root_nodes().order_by('code').values('code')


sitemaps = {
    'initiatives': InitiativeSitemap,
    'projects': ProjectSitemap,
    'recipients': RecipientSitemap,
    'agencies': AgencySitemap,
    'aid-type': AidTypeSitemap,
    'sectors': SectorSitemap,
}