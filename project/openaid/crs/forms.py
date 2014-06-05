from django import forms
from openaid.crs.models import Project, Markers, Activity

__author__ = 'joke2k'


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

class ActivityForm(forms.ModelForm):

    class Meta:
        model = Activity


class CodeListForm(forms.Form):

    id = forms.IntegerField(min_value=0)
    name = forms.CharField(max_length=500)


class MarkersForm(forms.ModelForm):

    class Meta:
        model = Markers