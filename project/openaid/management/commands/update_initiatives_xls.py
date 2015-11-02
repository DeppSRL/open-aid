# coding=utf-8
__author__ = 'stefano'
import logging
import re
from pprint import pprint
from optparse import make_option
from django.core.exceptions import ObjectDoesNotExist
from openpyxl import load_workbook
from django.core.management.base import BaseCommand
from openaid.codelists.models import Recipient
from openaid.projects.models import Initiative

# Opens xls file from MAE, update existing iniziative with total, grant and loan amount from file.
# Create new iniziative. Update all the initiatives not listed in the file: STATUS = COMPLETED

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--file',
                    dest='file',
                    default='',
                    help='path to input file'),
    )

    help = """
        Opens xls file from MAE, update existing iniziative with total, grant and loan amount from file.
        Create new iniziative. Update all the initiatives not listed in the file: STATUS = COMPLETED
        """
    logger = logging.getLogger('openaid')

    @staticmethod
    def find_recipient_from_name(name):
        from django.db.models import Q
        # deals with special cases recipient

        special_cases = {
            'Corea (Rep.Dem.Pop.)': '740',
            'Rep. Centro-Africana': '231',
            'Rep.Dem.Congo(Zaire)': '235',
            'Sadcc': '298',
            'Sahel': '289',
            'Territori Palestines': '550',
            'Yugoslavia': '88',
            'Italia': '998',
        }
        if name in special_cases.keys():
            return Recipient.objects.get(code=special_cases[name])

        # gets recipient, tries with italian and english name
        try:
            recipient = Recipient.objects.get(Q(name_it=name) | Q(name_en=name))
        except ObjectDoesNotExist:
            try:
                recipient = Recipient.objects.get(name__startswith=name[:4])
            except ObjectDoesNotExist:
                return None

        return recipient

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
        input_ws = input_workbook['Openaid']
        counters = {'recipient_not_found': 0, 'recipient_missing': 0, 'new_initiatives': 0}
        initiative_codes_found =[]
        unknown_recipients = {}
        row_counter = 0
        for row_counter, row in enumerate(input_ws.rows):
            initiative_code = row[0].value
            recipient = None

            if row_counter == 0 or initiative_code is None:
                continue

            # gets initiative code and zfill it
            initiative_code = str(initiative_code).zfill(6)
            # fills list of codes found to set to concluded the initiatives not listed in the file
            initiative_codes_found.append(initiative_code)
            title_it = row[3].value.strip()
            recipient_name = row[2].value
            # gets values for total, grant and loan
            total = float(row[5].value)
            grant = float(row[6].value)
            loan = float(row[7].value)

            try:
                initiative = Initiative.objects.get(code=initiative_code)
            except ObjectDoesNotExist:
                # if initiative not present in DB, try to insert it
                initiative = Initiative()

                self.logger.error(
                    "Initiative not found:'{}', row:{}, create a new one".format(initiative_code, row_counter))
                counters['new_initiatives'] += 1

                # gets recipient for new initiative

                if recipient_name == None or recipient_name == '':
                    self.logger.error("Recipient empty for row:{}".format(row_counter))
                    counters['recipient_missing'] += 1
                elif recipient_name.strip() == '(vuoto)' or recipient_name.strip().lower() == 'non ripartibile':
                    self.logger.error("Recipient empty for row:{}".format(row_counter))
                    counters['recipient_missing'] += 1

                else:
                    recipient_name = recipient_name.strip().title()
                    recipient_name_no_parentesis = re.sub(r'\([^)]*\)', '', recipient_name).strip()

                    recipient = self.find_recipient_from_name(recipient_name)
                    if recipient is None:
                        recipient = self.find_recipient_from_name(recipient_name_no_parentesis)
                        if recipient is None:
                            self.logger.error("Recipient not found:'{}', skip row".format(recipient_name))
                            counters['recipient_not_found'] += 1
                            if recipient_name not in unknown_recipients:
                                unknown_recipients[recipient_name] = 0
                            unknown_recipients[recipient_name] += 1
                            continue

                #     fills new Initiative with new data
                initiative.recipient_temp= recipient
                initiative.code = initiative_code
                initiative.title_it = title_it

            else:
                #     update initiative existing initiative only over writing total,grant,loan
                self.logger.debug(u"Updated initiative:{} with total,loan and grant".format(initiative_code))

            # for the new initiatives fill in loan, grant, total and save the obj
            # for the initiative already present: update these 3 fields and save the obj
            initiative.loan_amount_approved = loan
            initiative.grant_amount_approved= grant
            initiative.total_project_costs= total
            initiative.save()

        self.logger.info("Analyzed {} rows".format(row_counter, ))

        # setta tt le altre iniziative status=completed
        initiatives_not_listed = Initiative.objects.exclude(code__in=initiative_codes_found)
        initiatives_not_listed.update(status_temp ='100')
        self.logger.info("Updated {} initiatives not listed as COMPLETED".format(initiatives_not_listed.count()))

        # print errors
        self.logger.info("Type of errors found:")
        pprint(counters)

        if unknown_recipients != {}:
            self.logger.info("Unknown recipients found are:")
            pprint(unknown_recipients)
