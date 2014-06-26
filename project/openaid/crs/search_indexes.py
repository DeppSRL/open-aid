from django.conf import settings
from django.utils import translation
from haystack import indexes
from .models import Activity


translation.activate(settings.LANGUAGE_CODE)


class ActivityIndex(indexes.ModelSearchIndex, indexes.Indexable):

    fields_to_skip = indexes.ModelSearchIndex.fields_to_skip + (
        'usd_adjustment', 'usd_adjustment_defl', 'usd_amount_partialtied',
        'usd_amount_partialtied_defl', 'usd_amount_tied', 'usd_amount_tied_defl',
        'usd_amount_untied', 'usd_amount_untied_defl', 'usd_arrears_interest',
        'usd_arrears_principal', 'usd_commitment', 'usd_commitment_defl',
        'usd_disbursement', 'usd_disbursement_defl', 'usd_expert_commitment',
        'usd_expert_extended', 'usd_export_credit', 'usd_future_DS_interest',
        'usd_future_DS_principal', 'usd_interest', 'usd_outstanding',
        'usd_received', 'usd_received_defl',
    )

    text = indexes.CharField(document=True, use_template=True)
    project = indexes.CharField(model_attr='project', null=True)
    year = indexes.IntegerField(model_attr='year', faceted=True)

    def get_facets_counts(self):
        return self.objects.facet('year').facet_counts().get('fields', {})

    class Meta:
        model = Activity
