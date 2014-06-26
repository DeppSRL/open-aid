from django import forms
from django.utils.translation import ugettext_lazy as _
from haystack.forms import FacetedSearchForm
from openaid.crs.models import Project, Markers, Activity

__author__ = 'joke2k'

def text_cleaner(text):
    # http://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python
    return u' '.join(text.split())


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

class ActivityForm(forms.ModelForm):

    def clean_title(self):
        title = self.cleaned_data.get('title')
        return text_cleaner(title)

    def clean_description(self):
        description = self.cleaned_data.get('description')
        return text_cleaner(description)

    class Meta:
        model = Activity


class CodeListForm(forms.Form):

    id = forms.IntegerField(min_value=0)
    name = forms.CharField(max_length=500)


class MarkersForm(forms.ModelForm):

    class Meta:
        model = Markers


class FacetedActivitySearchForm(FacetedSearchForm):

    default_order = 'year'
    default_desc = True
    order_by = forms.ChoiceField(initial=default_order, required=False, choices=(
        ('year', _("Year")),
    ))
    desc = forms.BooleanField(initial=default_desc, required=False)

    def __init__(self, *args, **kwargs):
        super(FacetedActivitySearchForm, self).__init__(*args, **kwargs)
        self.fields['order_by'].widget.attrs.update({'class' : 'form-control'})

    def search(self):
        sqs = super(FacetedActivitySearchForm, self).search()

        data = {}

        if self.is_valid():
            data = self.cleaned_data

        order_field = data.get('order_by', None) or self.default_order
        is_desc = data.get('desc', self.default_desc)
        if is_desc:
            order_field = '-{0}'.format(order_field)

        return sqs.order_by(order_field)

    def no_query_found(self):
        """
        Retrieve all search results for empty query string
        """
        return self.searchqueryset.all()