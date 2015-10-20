# coding=utf-8
__author__ = 'stefano'
import logging
from django.core.management.base import BaseCommand
from openaid.projects.models import Initiative, Project


class Command(BaseCommand):
    help = 'Fills Initiative selected fields with data from the most recent Project.' \
           ' Plus links Reports, Problems, Doc, Photos objs to Initiative'
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

        # maps the field name between project (keys) and initiative (value)
        field_map = {
            'description': 'description_temp',
            'recipient': 'recipient_temp',
            'outcome': 'outcome_temp',
            'beneficiaries': 'beneficiaries_temp',
            'beneficiaries_female': 'beneficiaries_female_temp',
            'status': 'status_temp',
            'is_suspended': 'is_suspended_temp',
            'other_financiers': 'other_financiers_temp',
            'loan_amount_approved': 'loan_amount_approved',
            'grant_amount_approved': 'grant_amount_approved',
            'counterpart_authority': 'counterpart_authority_temp',
            'email': 'email_temp',
            'location': 'location_temp',
        }

        for initiative in Initiative.objects.all().order_by('code'):
            self.logger.info(u"Update Initiative:'{}'".format(initiative))

            for project_fieldname, initiative_fieldname in field_map.iteritems():

                # when dealing with loan and grant amount get the project values only if the initiative
                # values for loan/grant are not present
                if project_fieldname == 'loan_amount_approved' or project_fieldname == 'grant_amount_approved':
                    if getattr(initiative, initiative_fieldname) is not None:
                        self.logger.debug(u"Not going to update {} field because it is NOT NULL in Initiative".format(
                            initiative_fieldname))
                        continue

                field_value = initiative._get_first_project_value(project_fieldname)
                
                # STATUS: if the proj.status is == 100 => Almost completed
                # translates the value to 90 for Almost completed in Initiative
                # because in Initiative there is a status for "COMPLETED' which has value=100
                if project_fieldname == 'status' and field_value == '100' :
                    field_value = '90'

                if field_value is not None:
                    initiative.__setattr__(initiative_fieldname, field_value)

                initiative.save()
        self.logger.info(u"Finished updating {} initiatives".format(Initiative.objects.all().count()))
