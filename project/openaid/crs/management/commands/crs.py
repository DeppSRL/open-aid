# coding=utf-8
from django.core.management.base import LabelCommand
from openaid.crs.management import loaders


class Command(LabelCommand):
    args = '<crs_file crs_file ...>'
    help = 'Speficica i CRS file da lavorare'

    def handle_label(self, crs_filename, **options):
        """
        Gli argomenti forniti sono i nomi dei file CRS da lavorare
        """
        import time
        start_time = time.time()
        i = 0
        with open(crs_filename, 'r') as crs_file:
            for i, activity in enumerate(loaders.CRSFileLoader(crs_file, encoding='utf-8').load(), start=1):
                self.stdout.write("\rImported project: %d" % (i), ending='')
                self.stdout.flush()
        self.stdout.write("\nTotal rows: %d" % i)
        self.stdout.write("Execution time: %d seconds" % (time.time() - start_time))
