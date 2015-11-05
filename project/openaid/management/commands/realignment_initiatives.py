# coding=utf-8
__author__ = 'stefano'
import logging
from pprint import pprint
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from openpyxl import load_workbook, Workbook
from django.core.management.base import BaseCommand
from openaid.projects.models import Project, Activity, Initiative, NewProject


class Command(BaseCommand):

    help = 'realign initatives with those in the xls input file'
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

        workbook = Workbook()
        ws_output = workbook.create_sheet(index=0, title='sheet')
        input_workbook = load_workbook(input_file, data_only=True)
        input_ws = input_workbook['Foglio1']
        self.logger.info(u"start")
        self.logger.info(u"finish")
