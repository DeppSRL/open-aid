# coding=utf-8
__author__ = 'stefano'
import logging
from pprint import pprint
from optparse import make_option
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from openpyxl import load_workbook, Workbook
from django.core.management.base import BaseCommand
from openaid.projects.models import Project, Activity, Initiative

#opens xls file from MAE, check if initiative number is missing or present in DB

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--file',
                    dest='file',
                    default='',
                    help='path to input file'),
    )

    help = 'opens xls file from MAE, check if initiative number is missing or present in DB'
    logger = logging.getLogger('openaid')

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        input_filename = options['file']
        if verbosity == '0':
            self.logger.setLevel(logging.ERROR)
        elif verbosity == '1':
            self.logger.setLevel(logging.WARNING)
        elif verbosity == '2':
            self.logger.setLevel(logging.INFO)
        elif verbosity == '3':
            self.logger.setLevel(logging.DEBUG)

        self.logger.info(u"Opening input file: {}".format(input_filename))
        input_file = open(input_filename, 'rb')
        input_workbook = load_workbook(input_file, data_only=True)
        input_ws = input_workbook['File_Roberto.Sisto_144594008428']
        row_counter = 0
        not_found = 0
        for row in input_ws.rows:
            row_counter+=1
            if row_counter == 0:

                continue

            initiative_code = str(row[0].value).zfill(6)
            try:
                Initiative.objects.get(code=initiative_code)
            except ObjectDoesNotExist:
                #     prints err
                self.logger.error("Initiative not found:'{}'".format(initiative_code))
                not_found +=1

            except MultipleObjectsReturned:
                self.logger.error("Multiple initiative found:'{}'".format(initiative_code))

        self.logger.info("Analyzed {} rows, {} initiatives not found".format(row_counter, not_found))
