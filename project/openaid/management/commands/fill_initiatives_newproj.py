# coding=utf-8
__author__ = 'stefano'
import logging
from django.core.management.base import BaseCommand
from django.db.transaction import set_autocommit, commit
from openaid.projects.models import Initiative, Project, NewProject


class Command(BaseCommand):
    help = 'Fills Initiative selected fields with data from data from NewProject table plus Photos'
    logger = logging.getLogger('openaid')


    # maps the field name between new project (keys) and initiative (value)
    field_map = {
        'description': 'description_temp',

    }

    def update_fields(self, initiative):
        # loops on every field that has to be updated and updates if the conditions apply
        for project_fieldname, initiative_fieldname in self.field_map.iteritems():

            field_value = initiative._get_first_project_value(project_fieldname)

            if field_value is not None:
                initiative.__setattr__(initiative_fieldname, field_value)

        return initiative

    def update_related_objects(self, initiative):

        # updates photo set getting the photos from the new projects
        initiative.photo_set = initiative.photos()
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
        for index, new_project in enumerate(NewProject.objects.all().order_by('number')):
            self.logger.debug(u"Update new proj:'{}'".format(new_project))

            new_project = self.update_fields(new_project)

            new_project = self.update_related_objects(new_project)

            #         commits every N initiatives
            if index % 500 == 0:
                self.logger.info(u"Reached new proj:'{}'".format(new_project))
                commit()

        #             final commit
        commit()
        set_autocommit(True)
        self.logger.info(u"Finished transfering {} new proj".format(NewProject.objects.all().count()))