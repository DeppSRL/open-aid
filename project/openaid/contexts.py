from django.conf import settings
from django.db.models import Min, Max
from .codelists import models
from .projects import models as projects_models
from .projects.forms import FacetedProjectSearchForm

YEAR_FIELD = 'selected_year'
YEAR_GET_FIELD = 'year'
START_YEAR = projects_models.Activity.objects.aggregate(Min('year'))['year__min']
END_YEAR = projects_models.Activity.objects.aggregate(Max('year'))['year__max']

YEARS_RANGE_FIELD = 'years'
YEARS = range(START_YEAR, END_YEAR+1)

def project_context(request):

    return {
        'project_name': settings.PROJECT_NAME,
        'available_languages': map(lambda x: x[0], settings.LANGUAGES),
        'recipients': models.Recipient.objects.root_nodes().prefetch_related('children'),
        'sectors': models.Sector.objects.root_nodes(),
        'channels': models.Channel.objects.root_nodes(),
        'aids': models.AidType.objects.root_nodes(),
        YEAR_FIELD: request.GET.get(YEAR_GET_FIELD, END_YEAR),
        YEARS_RANGE_FIELD: YEARS,
        'search_form': FacetedProjectSearchForm(request.GET)
    }