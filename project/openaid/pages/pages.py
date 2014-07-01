# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.utils.translation import ugettext as _

#
# This file defines all the static pages
# A handle and a label is all that's needed
# ...
#

# footer: Open AID Italia
footer_oai_pages = OrderedDict([
            ('progetto', _(u'The project')),
            ('chi_siamo', _(u'Who we are')),
            ('contatti', _(u'Contacts')),
            ('privacy', _(u'Privacy and user\'s rights')),
            ('licenza', _(u'License of use')),
            ('links', _(u'Links')),
        ])

# footer: Come fare per
footer_comefare_pages = OrderedDict([
            ('cercare', _(u'Search a project')),
            ('accreditarsi', _(u'Register as an APS recipient')),
            ('votare_commentare', _(u'Voting and commenting a project')),
            ('diario', _(u'Write a post on a project\'s blog')),
        ])

# footer: OpenData Italia
footer_od_pages = OrderedDict([
            ('scarica_dati', _(u'Download the data')),
            ('api', _(u'API')),
            ('licenze_cc', _(u'CC Licenses')),
            ('dati_per_ricerca', _(u'Data fair use')),
            ('open_data_pa', _(u'PA\'s open data')),
        ])

# all merged into footer sections
footer_sections = OrderedDict([
    ('oai', footer_oai_pages),
    ('comefare', footer_comefare_pages),
    ('od', footer_od_pages),
])


# pages under cooperazione (with cooperazione, as well)
cooperazione_pages = OrderedDict([
            ('cooperazione_italiana', _(u'The Italian Development Cooperation')),
            ('busan_partnership', _(u'Busan partnership')),
            ('contesto_internazionale', _(u'The international context')),
            ('obiettivi_e_priorita', _(u'Objectives and Priorities')),
            ('sistema_italia', _(u'The Italia System')),
            ('buone_pratiche', _(u'Best practices')),
            ('millennium_goals', _(u'The Millennium Development Goals (MDGs)')),
            ('post_2015', _(u'The Post 2015 Development Agenda')),
        ])




