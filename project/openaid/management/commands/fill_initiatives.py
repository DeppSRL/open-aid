# coding=utf-8
__author__ = 'stefano'
import logging
from django.core.management.base import BaseCommand
from django.db.transaction import set_autocommit, commit
from openaid.projects.models import Initiative, Project


class Command(BaseCommand):
    help = 'Fills Initiative selected fields with data from the most recent Project.' \
           ' Plus links Reports, Problems, Doc, Photos objs to Initiative'
    logger = logging.getLogger('openaid')


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
        'sector': 'purpose_temp',
    }

    def update_fields(self, initiative):
        # loops on every field that has to be updated and updates if the conditions apply
        for project_fieldname, initiative_fieldname in self.field_map.iteritems():

            # when dealing with loan and grant amount get the project values only if the initiative
            # values for loan/grant are not present
            if project_fieldname == 'loan_amount_approved' or project_fieldname == 'grant_amount_approved':
                if getattr(initiative, initiative_fieldname) is not None and getattr(initiative,
                                                                                     initiative_fieldname) != 0:
                    self.logger.debug(u"Not going to update {} field because it is NOT NULL in Initiative".format(
                        initiative_fieldname))
                    continue

            field_value = initiative._get_first_project_value(project_fieldname)

            if project_fieldname == 'sector' and field_value is not None:
                if field_value.get_children().count() != 0:
                    self.logger.error("Initiative:{}. Cannot copy SECTOR VALUE: {} from Project, this Sector is not a leaf node! SKIP".format(initiative,field_value))
                    continue

            # STATUS: if the proj.status is == 100 => Almost completed
            # translates the value to 90 for Almost completed in Initiative
            # because in Initiative there is a status for "COMPLETED' which has value=100
            if project_fieldname == 'status' and field_value == '100':
                field_value = '90'

            if field_value is not None:
                initiative.__setattr__(initiative_fieldname, field_value)

        return initiative

    def update_related_objects(self, initiative):

        # updates documents and photo set getting the photos and docs from the projects
        initiative.document_set = initiative.documents()
        initiative.photo_set = initiative.photos()

        # updates reports and problems with initiative link (project link will later be removed by migrations)
        for r in initiative.reports():
            r.initiative = initiative
            r.save()

        for prob in initiative.problems():
            prob.initiative = initiative
            prob.save()

        return initiative

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


        set_autocommit(False)
        self.logger.info(u"Start procedure")
        for index, initiative in enumerate(Initiative.objects.all().order_by('code')):
            self.logger.debug(u"Update Initiative:'{}'".format(initiative))

            initiative = self.update_fields(initiative)

            initiative = self.update_related_objects(initiative)

            initiative.save()
            #         commits every N initiatives
            if index % 500 == 0:
                self.logger.info(u"Reached Initiative:'{}'".format(initiative))
                commit()

        #             final commit
        commit()
        set_autocommit(True)
        self.logger.info(u"Finished updating {} initiatives".format(Initiative.objects.all().count()))