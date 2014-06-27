# coding=utf-8
import time
from optparse import make_option
from django.core.management.base import BaseCommand
from django.db import transaction
from openaid.crs.management import loaders


class DryRunException(Exception):
    pass


class Command(BaseCommand):
    help = 'Importa le codelist da sdmx e dal modulo openaid.crs.code_lists'

    option_list = BaseCommand.option_list + (
        make_option('-n', '--dry-run',
            action='store_true', dest='dry_run', default=False,
            help="Do everything except modify the database."),
    )

    def handle(self, **options):

        start_time = time.time()
        i = 0
        try:
            with transaction.atomic():
                loaders.CodeListLoader().load()
                if options.get('dry_run', False):
                    raise DryRunException()

        except DryRunException:
            self.stdout.write("\nDry-Run correctly executed")

        self.stdout.write("\nTotal rows: %d" % i)
        self.stdout.write("Execution time: %d seconds" % (time.time() - start_time))
