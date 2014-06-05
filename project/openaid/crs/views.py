from django.views.generic import DetailView, ListView
from django.db.models import Count
from . import models

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