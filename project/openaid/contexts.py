from django.conf import settings
from django.db.models import Min, Max
from .crs import models


def project_context(request):

    return {
        'project_name': settings.PROJECT_NAME,
        'available_languages': map(lambda x: x[0], settings.LANGUAGES),
        'recipients': models.Region.objects.all().prefetch_related('recipient_set'),
        'sectors': models.Sector.objects.get(parent__isnull=True).children.all(),
        'channels': models.Channel.objects.filter(parent__isnull=True),
        'aids': models.AidType.objects.get(parent__isnull=True).children.all(),
    }