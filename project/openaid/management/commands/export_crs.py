# coding=utf-8
from collections import OrderedDict
import csv
from optparse import make_option
import time
from django.core.management.base import BaseCommand
from openaid.utils import UnicodeDictWriter
from openaid.projects.models import Activity


class Command(BaseCommand):
    help = 'Esporta i crs zippati'
    encoding = 'utf-8'
    output_filename = 'export.csv'

    option_list = BaseCommand.option_list + (
        make_option('-y', '--year', action='store', dest='year', default=None, type=int,
                    help='Select a specific year to export. If not provided one zip for each year will be created.'),
        make_option('-a', '--all', action='store_true', dest='all', default=False,
                    help='Export all activities in one file.'),
    )

    map = {
        'year': 'year',
        'pk': 'openaid id',
        'project__agency__donor__code': 'donorcode',
        'project__agency__donor__name': 'donorname',
        'project__agency__code': 'agencycode',
        'project__agency__name': 'agencyname',
        'project__crsid': 'crsid',
        'project__number': 'projectnumber', #usiamo questo o il number activity come nell'import?
        'proejct__activity__report_type': 'initialreport',
        'project__recipient__code': 'recipientcode',
        'project__recipient__name': 'recipientname',
        'project__recipient__parent__code': 'regioncode',
        'project__recipient__parent__name': 'regioname',

    }

    csv_fieldset = {
        'pk':'pk',
        'year':'year',
        'project__recipient__code':'project__recipient__code',
        'project__recipient__parent__code':'project__recipient__parent__code'
    }

    def write_file(self, activity_set):
        f = open(self.output_filename, "w")

        udw = UnicodeDictWriter(f, fieldnames=self.csv_fieldset.keys(), encoding=self.encoding)

        udw.writerow(self.csv_fieldset)

        for activity in activity_set:
            udw.writerow(activity)



    def export(self, focus):

        activity_set = Activity.objects.all()
        if focus != 'all':
            activity_set = activity_set.filter(year=int(focus))
        # activity_set = activity_set.values(*self.map.keys())
        activity_set = activity_set.values(*self.csv_fieldset.keys())

        self.write_file(activity_set)


    def handle(self, *args, **options):
        start_time = time.time()
        if options['all']:
            focus = 'all'
        elif options['year']:
            focus = options['year']
        else:
            focus = None
        try:

            self.export(focus)

        except KeyboardInterrupt:
            self.stdout.write("\nCommand execution aborted.")
        finally:
            self.stdout.write("Execution time: %d seconds" % (time.time() - start_time))
