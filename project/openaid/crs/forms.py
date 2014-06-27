from django import forms
from django.conf import settings
from django.utils.text import slugify
from openaid.crs.models import Project, Markers, Activity

__author__ = 'joke2k'

def text_cleaner(text):
    # http://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python
    return u' '.join(text.split()).strip(u' ')


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

    def clean_long_description(self):
        long_description = self.cleaned_data.get('long_description')
        return text_cleaner(long_description)

    def clean(self):
        data = super(ActivityForm, self).clean()

        if data['description']:
            if data['long_description'] and slugify(data['description']) == slugify(data['long_description']):
                data['long_description'] = ''

        if data['title']:
            if data['description'] and slugify(data['title']) == slugify(data['description']):
                data['description'] = ''

        return data

    class Meta:
        model = Activity


class CodeListForm(forms.Form):

    id = forms.IntegerField(min_value=0)
    name = forms.CharField(max_length=500)


class MarkersForm(forms.ModelForm):

    class Meta:
        model = Markers