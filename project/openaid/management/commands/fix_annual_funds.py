__author__ = 'stefano'
# coding=utf-8
from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from openaid.projects.models import AnnualFunds, Organization


class Command(BaseCommand):

    help = 'JUST FOR DEVELOPMENT: adds TYPE to organizations based on their names'
    logger = logging.getLogger('openaid')



    def handle(self, *args, **options):
        verbosity = options['verbosity']
        if verbosity == '0':
            self.logger.setLevel(logging.ERROR)
        elif verbosity == '1':
            self.logger.setLevel(logging.WARNING)
        elif verbosity == '2':
            self.logger.setLevel(logging.INFO)
        elif verbosity == '3':
            self.logger.setLevel(logging.DEBUG)
        #
        # ORGANIZATION_TYPES = Choices(
        #     (1, _('UN agencies')),
        #     (2, _('EU institutions')),
        #     (3, _('IDA')),
        #     (4, _('Other World Bank (IBRD,IFC,MIGA)')),
        #     (5, _('Regional development banks')),
        #     (6, _('Other agencies')),
        #     (7, _('Global Environment Facility (96%)')),
        #     (8, _('Montreal Protocol')),
        # )

        mapping = {
            'UN agencies':1,
            'EU institutions':2,
            'IDA':3,
            'Other World Bank (IBRD,IFC,MIGA)':4,
            'World Trade Organisation':4,
            'World Trade Organization':4,
            'Regional development banks':5,
            'Other agencies':6,
            'Global Environment Facility (96%)':7,
            'Montreal Protocol':8,
        }

        all_org = Organization.objects.filter(type__isnull=True, annualfunds__isnull=False)
        for org in all_org:
            try:
                org.type = mapping[org.name]
            except KeyError:
                self.logger.error("key:'{}' not found in mapping".format(org.name))
            org.save()
        self.logger.info("Updated:{} annual funds".format(all_org.count()))
