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

def prepare_codelist(items):
    return set([i.code for i in items if i])

class ProjectIndex(indexes.ModelSearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    # facets
    years = indexes.FacetMultiValueField()
    # facets for code-lists
    recipient = indexes.FacetCharField()
    agencies = indexes.FacetMultiValueField()
    aid_types = indexes.FacetMultiValueField()
    channels = indexes.FacetMultiValueField()
    finance_types = indexes.FacetMultiValueField()
    sectors = indexes.FacetMultiValueField()

    def prepare_years(self, obj):
        return obj.years_range()
    def prepare_recipient(self, obj):
        return obj.recipient.code

    def _prepare_codelist(self, items, roots=True):
        if roots:
            items = only_roots(items)
        return list(set([i.code for i in items if i]))

    def prepare_agencies(self, obj):
        return self._prepare_codelist(obj.agencies(), roots=False)
    def prepare_aid_types(self, obj):
        return self._prepare_codelist(obj.aid_types())
    def prepare_channels(self, obj):
        return self._prepare_codelist(obj.channels())
    def prepare_finance_types(self, obj):
        return self._prepare_codelist(obj.finance_types())
    def prepare_sectors(self, obj):
        return self._prepare_codelist(obj.sectors())

    def get_facets_counts(self):
        return self.objects.facet('year').facet_counts().get('fields', {})

    class Meta:
        model = Project
        excludes = ['is_suspended', 'status', 'expected_start_year', 'expected_completion_year','expected_start_date', 'completion_date',
                    'last_update', 'outcome', 'beneficiaries', 'beneficiaries_female',
                    'total_project_costs', 'other_financiers', 'loan_amount_approved',
                    'grant_amount_approved', 'counterpart_authority', 'email', 'location',
                    'description', 'title', 'title_it', 'title_en', 'description_it', 'description_en', 'number',
                    'outcome_it', 'beneficiaries_it', 'other_financiers_it', 'counterpart_authority_it', 'location_it',
                    'outcome_en', 'beneficiaries_en', 'other_financiers_en', 'counterpart_authority_en', 'location_en']
