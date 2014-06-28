# coding=utf-8
from os import path
import time
import csvkit
from django.core.management.base import LabelCommand, CommandError
from django.conf import settings
from openaid.codelists import models


class Command(LabelCommand):

    ACTIONS = ['import', 'reload', 'clear', 'translate', 'stats']

    args = '|'.join(ACTIONS)
    help = 'Execute an action on code lists.'

    def handle_label(self, action, **options):

        assert action in self.ACTIONS

        if action == 'stats':
            self.handle_stats(**options)
            return

        elif action == 'clear':
            self.delete_code_lists()

        elif action == 'translate':
            raise CommandError("Not implemented")

        elif action in ('reload', 'import'):
            counters = self.get_code_list_counters()
            already_imported = any([c for cl, c in counters])
            if action == 'import' and already_imported:
                self.stderr.write('\nError: Code lists already exists. Try to use `manage.py codelists reload`.')
                return

            if already_imported:
                self.delete_code_lists()

            for codelist in models.CODE_LISTS:
                self.import_codelist(codelist)

    def handle_stats(self, **options):
        for codelist, count in self.get_code_list_counters():
            self.stdout.write('%s: %d' % (codelist.code_list, count))

    ## utils
    def import_codelist(self, codelist):

        i = 0
        start_time = time.time()
        self.stdout.write('\n### IMPORT CODELIST: %s' % codelist.code_list)
        csv_path = path.join(settings.RESOURCES_PATH, 'codelists', '%s.csv' % codelist.code_list)
        reader = csvkit.DictReader(open(csv_path))
        for row in reader:
            # agency has donor
            if codelist.code_list == 'agency':
                # skip other agencies (code is unique)
                if int(row['donor']) != settings.OPENAID_CRS_DONOR:
                    continue
                row['donor'] = models.Donor.objects.get(code=row['donor'])
            if row.has_key('parent'):
                try:
                    row['parent'] = codelist.objects.get(code=row['parent'])
                except codelist.DoesNotExist:
                    row['parent'] = None
            codelist.objects.create(**row)
            i += 1

        self.stdout.write("Total rows: %d" % i)
        self.stdout.write("Execution time: %d seconds" % (time.time() - start_time))
        self.stdout.write('###\n')


    def delete_code_lists(self):
        answer = raw_input('Are you sure? (Yes/No)')
        if answer.lower() in ('yes', 'y'):
            for CodeList in self.get_code_lists():
                self.stdout.write('\nDeleting %s' % CodeList.code_list)
                self.stdout.write(': %d' % CodeList.objects.count())
                CodeList.objects.all().delete()

    def get_code_list_counters(self):
        return [(cl, cl.objects.count()) for cl in models.CODE_LISTS]

    def get_code_lists(self):
        return models.CODE_LISTS

