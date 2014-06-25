# coding=utf-8
import time
from optparse import make_option
from django.core.management.base import LabelCommand
from django.db import transaction
from openaid.crs.management import loaders


class DryRunException(Exception):
    pass


class Command(LabelCommand):
    args = 'csvfile title|description'
    help = 'Specifica il tipo di traduzione da importare.'

    option_list = LabelCommand.option_list + (
        make_option('-f', '--field',
            action='store', dest='field', default='title',
            help="Translated field."),
        make_option('-n', '--dry-run',
            action='store_true', dest='dry_run', default=False,
            help="Do everything except modify the database."),
    )

    def handle_label(self, crs_file, **options):

        start_time = time.time()
        i = 0
        translations = 0
        field = options.get('field')
        with open(crs_file, 'r') as crs_file:
            try:
                with transaction.atomic():
                    for i, (value, activities) in enumerate(loaders.ActivityTranslator(crs_file, field=field, encoding='utf-8').translate(), start=1):
                        if activities == 0:
                            self.stdout.write("\rActivity not found for row %d: '%s'" % (i, value))
                        else:
                            self.stdout.write("\r%s: Translated activities %d" % (i, activities), ending='')
                            self.stdout.flush()
                        translations += activities
                    if options.get('dry_run', False):
                        raise DryRunException()

            except DryRunException:
                self.stdout.write("\nDry-Run correctly executed")

        self.stdout.write("\nTotal rows: %d" % i)
        self.stdout.write("Execution time: %d seconds" % (time.time() - start_time))
