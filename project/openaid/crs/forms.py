from django import forms
from django.conf import settings
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