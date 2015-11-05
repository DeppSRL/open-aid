# coding=utf-8
from optparse import make_option

__author__ = 'stefano'
import logging
from pprint import pprint
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from openpyxl import load_workbook, Workbook
from django.core.management.base import BaseCommand
from openaid.projects.models import Project, Activity, Initiative, NewProject


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--file',
                    dest='file',
                    default='',
                    help='path to input file'),
    )


    help = 'realign initatives with those in the xls input file'
    logger = logging.getLogger('openaid')
    stash_codici = []
    completed_only_xls = []
    completed_in_xls = []
    corso_only_xls = []
    corso_in_xls = []

    def check_uniqueness(self,ws):
        ret = False
        for row_counter, row in enumerate(ws.rows):
            if row_counter == 0:
                continue
            codice = row[0].value
            if codice is None:
                continue
            if codice in self.stash_codici:
                self.logger.error("Row:{} - Codice '{}' non univoco!".format(row_counter,codice))
                ret = True
            else:
                self.stash_codici.append(codice)

        return ret

    def examinate_completed(self, ws):
        for row_counter, row in enumerate(ws.rows):
            if row_counter == 0:
                continue
            code = str(row[0].value).zfill(6)
            if code not in self.completed_in_xls:
                self.completed_in_xls.append(code)
            try:
                initiative = Initiative.objects.get(code=code)
            except ObjectDoesNotExist:
                self.completed_only_xls.append(code)
                continue
            else:
                total = row[3].value
                grant = row[4].value
                loan = row[5].value
                initiative.status_temp = '100'
                initiative.total_project_costs = total
                initiative.loan_amount_approved = loan
                initiative.grant_amount_approved = grant
                initiative.save()

        # print out codes present ONLY in XLS
        if len(self.completed_only_xls) > 0:
            string_codes = ",".join(self.completed_only_xls)
            self.logger.error("COMPLETED: codes only in XLS:{}".format(string_codes))

        # print out codes present ONLY in DB
        completed_missing_xls = Initiative.objects.filter(status_temp='100').exclude(code__in=self.completed_in_xls).order_by('code').values_list('code',flat=True)
        if len(completed_missing_xls) > 0:
            string_codes = ",".join(completed_missing_xls)
            self.logger.error("COMPLETED: codes only in DB:{}".format(string_codes))



    def examinate_in_corso(self, ws):
        for row_counter, row in enumerate(ws.rows):
            if row_counter == 0:
                continue

            code = row[0].value

            if code is None:
                continue
            code = str(code).zfill(6)
            if code not in self.corso_in_xls:
                self.corso_in_xls.append(code)

            try:
                initiative = Initiative.objects.get(code=code)
            except ObjectDoesNotExist:
                self.corso_only_xls.append(code)
                continue
            else:
                if initiative.status_temp == '100':
                    self.logger.info("IN CORSO: update status iniziativa:{} to Not available".format(code))
                    initiative.status_temp = '-'
                    initiative.save()

    def log_in_corso(self):
        # print out codes present ONLY in XLS
        if len(self.corso_only_xls) > 0:
            string_codes = ",".join(self.corso_only_xls)
            self.logger.error("IN CORSO: codes only in XLS:{}".format(string_codes))

        # print out codes present ONLY in DB
        self.logger.debug("There are {} initiatives in corso in xls".format(len(self.corso_in_xls)))
        corso_missing_xls = Initiative.objects.all().exclude(status_temp='100').exclude( code__in=self.corso_in_xls).order_by('code').values_list('code',flat=True)
        if len(corso_missing_xls) > 0:
            string_codes = ",".join(corso_missing_xls)
            self.logger.error("IN CORSO: codes only in DB:{}".format(string_codes))



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
        ws_esecuzione_con_scheda = input_workbook['In esecuzione con scheda']
        ws_esecuzione_senza_scheda = input_workbook['In esecuzione senza scheda']
        ws_completed = input_workbook['Chiuse']

        self.logger.info("Checking uniqueness of codes in the file")
        # check that codes are unique in the whole file, initiatives cannot be repeated
        self.logger.info("Checking iniziative esecuzione con scheda")
        ret1 = self.check_uniqueness(ws_esecuzione_con_scheda)
        self.logger.info("Checking iniziative esecuzione senza scheda")
        ret2 = self.check_uniqueness(ws_esecuzione_senza_scheda)
        self.logger.info("Checking iniziative completed")
        ret3 = self.check_uniqueness(ws_completed)

        if ret1 or ret2 or ret3:
            self.logger.critical("Codes are not unique in the file. Quitting")
            # exit()
        else:
            self.logger.info("All codes are unique")

        # deal with completed initiatives
        self.logger.info("Examinate COMPLETED sheet")
        self.examinate_completed(ws_completed)
        self.logger.info("Examinate IN CORSO sheet")
        # deal with in corso initiatives
        self.examinate_in_corso(ws_esecuzione_con_scheda)
        self.examinate_in_corso(ws_esecuzione_senza_scheda)
        self.log_in_corso()

        self.logger.info(u"finish")
