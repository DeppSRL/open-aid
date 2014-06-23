from django.conf import settings


def project_context(request):
    return {
        'project_name': settings.PROJECT_NAME,
        'available_languages': map(lambda x: x[0], settings.LANGUAGES),
    }