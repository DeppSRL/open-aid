# coding=utf-8
__author__ = 'stefano'
import logging
from optparse import make_option
from pprint import pprint
from django.core.exceptions import ObjectDoesNotExist
from openpyxl import load_workbook
from django.core.management.base import BaseCommand
from openaid.projects.models import Initiative


class Command(BaseCommand):
    option_list = BaseCommand.option_list

    help = 'import financial data for initiatives. 1 dec 2015 only'
    logger = logging.getLogger('openaid')
    stash_codici = []
    completed_only_xls = []
    completed_in_xls = []
    corso_only_xls = []
    corso_in_xls = []

    def get_code(self, row):
        code = None
        zfill_code = None
        value = row[0].value
        if type(value) == int:
            code = value
        if type(value) == float:
            try:
                code = int(value)
            except TypeError:
                return None, None

        zfill_code = str(code).zfill(6)
        return code, zfill_code


    def convert_list_to_string(self, list):
        return ",".join(list)

    def check_uniqueness(self,ws):
        ret = False
        for row_counter, row in enumerate(ws.rows):
            if row_counter == 0:
                continue
            code, zfill_code = self.get_code(row)
            if code is None:
                continue

            if zfill_code in self.stash_codici:
                self.logger.error("Row:{} - Codice '{}' non univoco!".format(row_counter,code))
                ret = True
            else:
                self.stash_codici.append(zfill_code)
        return ret

    def examinate_in_corso(self, ws):
        for row_counter, row in enumerate(ws.rows):
            if row_counter == 0:
                continue

            code, zfill_code = self.get_code(row)
            if code is None:
                continue
            if zfill_code not in self.corso_in_xls:
                self.corso_in_xls.append(zfill_code)

            try:
                initiative = Initiative.objects.get(code=zfill_code)
            except ObjectDoesNotExist:
                self.corso_only_xls.append(zfill_code)
                continue
            else:
                self.logger.info("Update financial data for init:{}".format(initiative.code))
                total = row[6].value
                grant = row[5].value
                loan = row[4].value
                initiative.total_project_costs = total
                initiative.loan_amount_approved = loan
                initiative.grant_amount_approved = grant
                if initiative.status_temp == '100':
                    self.logger.info("Update STATUS for init:{}".format(initiative.code))
                    initiative.status_temp = '-'
                initiative.save()

    def log_in_corso(self):
        # print out codes present ONLY in XLS
        if len(self.corso_only_xls) > 0:
            self.logger.error("IN CORSO: codes only in XLS:{}".format(self.convert_list_to_string((self.corso_in_xls))))

        # print out codes present ONLY in DB
        self.logger.debug("There are {} initiatives in corso in xls".format(len(self.corso_in_xls)))
        corso_missing_xls = Initiative.objects.all().exclude(status_temp='100').exclude( code__in=self.corso_in_xls).order_by('code').values_list('code',flat=True)
        if len(corso_missing_xls) > 0:
            self.logger.error("IN CORSO: codes only in DB:{}".format(self.convert_list_to_string((corso_missing_xls))))

    def check_subsets(self):
        #     check what are the codes only in the XLS, and then check which are the codes only in the DB
        codes_db = set(Initiative.objects.all().exclude(status_temp='100').order_by('code').values_list('code',flat=True))
        codes_xls = set(self.stash_codici)

        stringa_db = self.convert_list_to_string(codes_db-codes_xls)
        stringa_xls = self.convert_list_to_string(codes_xls-codes_db)

        self.logger.info("DB-XLS:{}".format(stringa_db))
        self.logger.info("XLS-DB:{}".format(stringa_xls))

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        input_filename = 'resources/fixtures/Aid.Titolo.Iniziative.Stato.Finanziario.DGCS.251115.xlsx'
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
        input_workbook = load_workbook(input_file, data_only=True, use_iterators = True)
        ws_esecuzione_con_scheda = input_workbook['Esecuzione con scheda']
        ws_esecuzione_senza_scheda = input_workbook['Esecuzione senza scheda']

        self.logger.info("Checking uniqueness of codes in the file")
        # check that codes are unique in the whole file, initiatives cannot be repeated
        self.logger.info("Checking iniziative esecuzione con scheda")
        ret1 = self.check_uniqueness(ws_esecuzione_con_scheda)
        self.logger.info("Checking iniziative esecuzione senza scheda")
        ret2 = self.check_uniqueness(ws_esecuzione_senza_scheda)

        if ret1 or ret2:
            self.logger.critical("Codes are not unique in the file. Quitting")
            exit()
        else:
            self.logger.info("All codes are unique")

        self.logger.info("Examinate IN ESECUZIONE sheet")
        # deal with in corso initiatives
        self.examinate_in_corso(ws_esecuzione_con_scheda)
        self.examinate_in_corso(ws_esecuzione_senza_scheda)
        self.check_subsets()
        # log the results
        self.log_in_corso()

        self.logger.info(u"finish")
