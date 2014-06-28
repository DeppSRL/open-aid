# -*- coding: utf-8 -*-
from .views import CooperazioneView, StaticPageView
from django.conf.urls import patterns, url, include
from .pages import  footer_sections, cooperazione_pages


urls = []

for section_id, footer_section_pages in footer_sections.items():
    for page_url_name, page_label in footer_section_pages.items():
        urls.append(
            url(r"^{0}$".format(page_url_name.replace('_', '-')),
                StaticPageView.as_view(
                    template_name="footer_{0}_{1}.html".format(section_id, page_url_name),
                    page_url_name=page_url_name,
                    page_label=page_label
                ),
                name=page_url_name
            )
        )


for page_url_name, page_label in cooperazione_pages.items():
    urls.append(
        url(r"^{0}$".format(page_url_name.replace('_', '-')),
            CooperazioneView.as_view(
                template_name="coop_{0}.html".format(page_url_name),
                page_url_name=page_url_name,
                page_label=page_label
            ),
            name=page_url_name
        )
    )

urlpatterns = patterns('', *urls)
