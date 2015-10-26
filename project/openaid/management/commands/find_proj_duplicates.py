# coding=utf-8
__author__ = 'stefano'
import logging
from django.core.management.base import BaseCommand
from openaid.projects.models import Initiative, Project


class Command(BaseCommand):
    help = 'Prints out project belonging to the same initiative that have different not-null values for certain fields.'
    logger = logging.getLogger('openaid')
    # fields to check arranged in a way to be used as a filter
    fields = [{'description_it__isnull':False},{'description_en__isnull':False},{'recipient__isnull':False},{'outcome_it__isnull':False},{'outcome_en__isnull':False},{'beneficiaries_it__isnull':False},{'beneficiaries_en__isnull':False},{'beneficiaries_female__isnull':False},{'status__isnull':False},{'is_suspended__isnull':False},{'other_financiers_it__isnull':False},{'other_financiers_en__isnull':False},{'loan_amount_approved__isnull':False},{'grant_amount_approved__isnull':False},{'counterpart_authority_it__isnull':False},{'counterpart_authority_en__isnull':False},{'email__isnull':False},{'location_en__isnull':False},{'location_it__isnull':False},{'sector__isnull':False}]

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


        self.logger.info(u"Start procedure")
        for field in self.fields:
            for init in Initiative.objects.all().order_by('code'):
                project_set = Project.objects.filter(initiative=init).filter(**field)
                count = project_set.count()
                if count > 1:
                    proj_pks = ",".join(project_set.values('pk',flat=True))
                    self.logger.error(u"Field:{}, count:{}, Initiative:{}, Projects:{}".format(field, count, init, proj_pks))

        self.logger.info(u"Finished")