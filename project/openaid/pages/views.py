# -*- coding: utf-8 -*-
import urls

from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView
from django.conf import settings

class StaticPageView(TemplateView):
    """
    This view extends (monkey-patches, more precisely),
    the TemplateResponseMixin's get_template_names,
    in order to intercept the currently selected language code
    and modify the template_name.

    It is assumed that the templates will go under dedicated directory,
    named after the language codes, i.e.:

        - en
          - footer_chi_siamo.html
          - contatti.html
        - it
          - footer_chi_siamo.html
          - contatti.html

    """
    template_language = None
    page_url_name = None
    page_label = {}

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.template_language is None:
            if self.request.LANGUAGE_CODE is None:
                raise ImproperlyConfigured(
                    "I18NTemplateView requires either a definition of "
                    "'template_language' or an implementation of 'get_template_language()'")
            else:
                self.template_language = self.request.LANGUAGE_CODE


        configured_languages = dict(settings.LANGUAGES).keys()
        if self.template_language is None:
            raise ImproperlyConfigured(
                "I18NTemplateView requires 'template_language' "
                "to be in one of the languages specified in the settings")

        if self.template_name is None:
            raise ImproperlyConfigured(
                "I18NTemplateView requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")

        return ["{0}/{1}".format(self.template_language, self.template_name)]

    def get_context_data(self, **kwargs):
        context = super(StaticPageView, self).get_context_data(**kwargs)
        context['page_label'] = self.page_label
        context['page_url_name'] = self.page_url_name
        return context


class CooperazioneView(StaticPageView):
    """
    This view extends the I18NTemplateView, and is used to show
    the pages under cooperaizone_italiana.

    Basically, it injects a cooperazione_pages key, within the context.

    The cooperazione_pages is imported from the urls module (in this pages package)
    """

    def get_context_data(self, **kwargs):
        context = super(CooperazioneView, self).get_context_data(**kwargs)
        context['cooperazione_pages'] = urls.cooperazione_pages
        return context
