__author__ = 'stefano'
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from openaid.codelists.models import Agency

class AgencyListFilter(admin.SimpleListFilter):

    title = _('Agency')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'agency'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return Agency.objects.filter(project__isnull=False).distinct().order_by('name').values_list('code','name',)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            agency_code = self.value()
            return queryset.filter(project__agency__code=str(agency_code))
