# coding=utf-8
from optparse import make_option
import time
from django.core.management.base import BaseCommand
from openaid.management import exporters

class Command(BaseCommand):
    help = 'Esporta i crs zippati'

    option_list = BaseCommand.option_list + (
        make_option('-y', '--year', action='store', dest='year', default=None, type=int,
            help='Select a specific year to export. If not provided one zip for each year will be created.'),
        make_option('-a', '--all', action='store_true', dest='all', default=False,
            help='Export all activities in one file.'),
    )

    def handle(self, *args, **options):
        start_time = time.time()
        if options['all']:
            focus = 'all'
        elif options['year']:
            focus = options['year']
        else:
            focus = None
        try:

            exporters.export_activities(focus)

        except KeyboardInterrupt:
            self.stdout.write("\nCommand execution aborted.")
        finally:
            self.stdout.write("Execution time: %d seconds" % (time.time() - start_time))
