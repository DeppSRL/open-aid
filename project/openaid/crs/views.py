from django.views.generic import DetailView, ListView, TemplateView
from django.db.models import Count, Max, Min, Sum
from . import models

class Home(TemplateView):
    template_name = 'crs/home.html'

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


class ProjectDetail(DetailView):
    model = models.Project

class ProjectList(ListView):
    model = models.Project
    paginate_by = 50

    def get_queryset(self):

        order_by = self.request.GET.get('order_by', None)
        # add `activities_count` field to project
        queryset = super(ProjectList, self).get_queryset().annotate(
            activities_count=Count('activity')
        )

        for valid_filter in ('recipient', 'crs'):
            if valid_filter in self.request.GET:
                queryset = queryset.filter(**{
                    valid_filter: self.request.GET.get(valid_filter)
                })

        if order_by:
            direction = ''
            if order_by.startswith('-'):
                direction, order_by = order_by[0], order_by[1:]
            if order_by in ('activities', 'crs', 'recipient'):
                if order_by == 'activities':
                    return queryset.order_by('{0}activities_count'.format(direction))
                queryset = queryset.order_by("{0}{1}".format(direction, order_by))
        return queryset
class ActivityDetail(DetailView):
    model = models.Activity

class ActivityList(ListView):
    model = models.Activity
    paginate_by = 50

class ProjectActivityList(ActivityList):

    def get_queryset(self):
        project_pk = self.kwargs.get('pk')
        return super(ProjectActivityList, self).get_queryset().filter(project=int(project_pk))