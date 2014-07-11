# coding=utf-8
import time
from django.core.management.base import NoArgsCommand
from openaid.management import exporters

class Command(NoArgsCommand):
    help = 'Esporta i crs zippati'

    def handle_noargs(self, **options):
        start_time = time.time()
        try:

            exporters.export_activities()

        except KeyboardInterrupt:
            self.stdout.write("\nCommand execution aborted.")
        finally:
            self.stdout.write("Execution time: %d seconds" % (time.time() - start_time))
