from django.conf import settings
from django.db.models import Min, Max
from openaid.pages import urls as pages_urls
from .crs import models

YEAR_FIELD = 'selected_year'
YEAR_GET_FIELD = 'year'
START_YEAR = models.Activity.objects.aggregate(Min('year'))['year__min']
END_YEAR = models.Activity.objects.aggregate(Max('year'))['year__max']

YEARS_RANGE_FIELD = 'years'
YEARS = range(START_YEAR, END_YEAR+1)

def project_context(request):

    return {
        'project_name': settings.PROJECT_NAME,
        'available_languages': map(lambda x: x[0], settings.LANGUAGES),
        'recipients': models.Region.objects.all().prefetch_related('recipient_set'),
        'sectors': models.Sector.objects.get(parent__isnull=True).children.all(),
        'channels': models.Channel.objects.filter(parent__isnull=True),
        'aids': models.AidType.objects.get(parent__isnull=True).children.all(),
        'footer_sections': pages_urls.footer_sections,
        YEAR_FIELD: request.GET.get(YEAR_GET_FIELD, END_YEAR),
        YEARS_RANGE_FIELD: YEARS,
    }