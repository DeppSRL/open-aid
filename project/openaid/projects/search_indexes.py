from haystack import indexes
from .models import Project


def only_roots(objects):
    roots = []
    for obj in objects:
        if not obj:
            continue
        if not obj.is_root_node():
            obj = obj.get_root()
        roots.append(obj)
    return list(set(roots))

class ProjectIndex(indexes.ModelSearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField()
    description = indexes.CharField()
    long_description = indexes.CharField()
    geography = indexes.CharField()

    # facets
    years = indexes.FacetMultiValueField()

    def prepare_years(self, obj):
        return obj.years_range()

    # facets for code-lists
    recipients = indexes.FacetMultiValueField()
    agencies = indexes.FacetMultiValueField()
    aid_types = indexes.FacetMultiValueField()
    channels = indexes.FacetMultiValueField()
    finance_types = indexes.FacetMultiValueField()
    sectors = indexes.FacetMultiValueField()

    def prepare_recipients(self, obj):
        return obj.recipients()
    def prepare_agencies(self, obj):
        return obj.agencies()
    def prepare_aid_types(self, obj):
        return only_roots(obj.aid_types())
    def prepare_channels(self, obj):
        return only_roots(obj.channels())
    def prepare_finance_types(self, obj):
        return only_roots(obj.finance_types())
    def prepare_sectors(self, obj):
        return only_roots(obj.sectors())

    def get_facets_counts(self):
        return self.objects.facet('year').facet_counts().get('fields', {})

    class Meta:
        model = Project
