# coding=utf-8
import time
from django.core.management.base import LabelCommand
from django.db import transaction
from openaid.crs.management import loaders


class DryRunException(Exception):
    pass


class Command(LabelCommand):
    args = '<crs_file crs_file ...>'
    help = 'Speficica i CRS file da lavorare'

    def handle_label(self, crs_filename, **options):
        """
        Gli argomenti forniti sono i nomi dei file CRS da lavorare
        """
        start_time = time.time()
        i = 0
        with open(crs_filename, 'r') as crs_file:
            try:
                with transaction.atomic():
                    for i, activity in enumerate(loaders.CRSFileLoader(crs_file, encoding='utf-8').load(), start=1):
                        self.stdout.write("\rImported project: %d" % (i), ending='')
                        self.stdout.flush()
                    if options.get('dry_run', False):
                        raise DryRunException()

            except DryRunException:
                self.stdout.write("\nDry-Run correctly executed")

        self.stdout.write("\nTotal rows: %d" % i)
        self.stdout.write("Execution time: %d seconds" % (time.time() - start_time))
