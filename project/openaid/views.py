from django.db.models import Min, Max, Sum
from django.views.generic import TemplateView
from .crs import models

class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):

        context = {
            'projects_count': models.Project.objects.count(),
            'activities_count': models.Activity.objects.count(),
            'recipients_count': models.Project.objects.values('recipient').distinct().count(),
            'start_year': models.Activity.objects.aggregate(Min('year'))['year__min'],
            'end_year': models.Activity.objects.aggregate(Max('year'))['year__max'],
            'usd_commitment_sum': models.Activity.objects.aggregate(Sum('usd_commitment'))['usd_commitment__sum'],
            'usd_disbursement_sum': models.Activity.objects.aggregate(Sum('usd_disbursement'))['usd_disbursement__sum'],
        }

        kwargs.update(context)

        return super(Home, self).get_context_data(**kwargs)