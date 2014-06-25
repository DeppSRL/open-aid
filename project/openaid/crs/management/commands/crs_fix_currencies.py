# coding=utf-8
import time
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from ... import models
from ... import utils


class DryRunException(Exception):
    pass


class Command(BaseCommand):
    help = 'Converte dove necessario i valori dei campi usd_*. ' \
           'Utilizza settings.OPENAID_CURRENCY lo confronta con la currency dell\'activity ' \
           'e se e diversa la converte grazie a settings.OPENAID_CURRENCY_CONVERSIONS'

    option_list = BaseCommand.option_list + (
        make_option('-n', '--dry-run',
            action='store_true', dest='dry_run', default=False,
            help="Do everything except modify the database."),
    )

    def handle(self, *args, **options):

        start_time = time.time()

        self.stdout.write("Currency: %s" % settings.OPENAID_CURRENCY)
        self.stdout.write("Activities: %s" % models.Activity.objects.count())
        self.stdout.write("Currencies found: %s" % set(models.Activity.objects.values_list('currency', flat=True).distinct()))
        self.stdout.write("Activities to convert: %s" % models.Activity.objects.exclude(currency=settings.OPENAID_CURRENCY).count())

        converted_activities = 0
        error_activities = 0

        try:
            with transaction.atomic():
                for i, activity in enumerate(models.Activity.objects.exclude(currency=settings.OPENAID_CURRENCY), start=1):

                    try:
                        results = utils.currency_converter(activity, save=True)
                        if len(results) > 0:
                            converted_activities += 1

                        self.stdout.write("\rActivity converted %s" % (i, ), ending='')
                        self.stdout.flush()
                    except utils.CurrencyConverterError as e:
                        self.stderr.write('\nError: %s' % e.message)
                        error_activities += 1
                        continue

                if options.get('dry_run'):
                    raise DryRunException()

        except DryRunException:
            self.stdout.write("\nDry-Run correctly executed")

        self.stdout.write("\nConverted activities: %d" % converted_activities)
        self.stdout.write("\nError activities: %d" % error_activities)
        self.stdout.write("\nTotal rows: %d" % i)
        self.stdout.write("Execution time: %d seconds" % (time.time() - start_time))
