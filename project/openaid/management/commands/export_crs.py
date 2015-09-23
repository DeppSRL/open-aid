# coding=utf-8
from collections import OrderedDict
import csv
import logging
from pprint import pprint
from optparse import make_option
import time
from django.core.management.base import BaseCommand
from openaid.utils import UnicodeDictWriter
from openaid.projects.models import Activity


class Command(BaseCommand):
    help = 'Esporta i crs zippati'
    encoding = 'utf-8'
    output_filename = 'export.csv'
    logger = logging.getLogger('openaid')

    option_list = BaseCommand.option_list + (
        make_option('-y', '--year', action='store', dest='year', default=None, type=int,
                    help='Select a specific year to export. If not provided one zip for each year will be created.'),
        make_option('-a', '--all', action='store_true', dest='all', default=False,
                    help='Export all activities in one file.'),
    )

    field_map = {
        'year': 'year',
        'project__agency__donor__code': 'donorcode',
        'project__agency__donor__name': 'donorname',
        'project__agency__code': 'agencycode',
        'project__agency__name': 'agencyname',
        'project__crsid': 'crsid',
        'number': 'projectnumber',
        'report_type': 'initialreport',
        'project__recipient__code': 'recipientcode',
        'project__recipient__name': 'recipientname',
        'project__recipient__parent__code': 'regioncode',
        'project__recipient__parent__name': 'regioname',
        'project__recipient__income_group': 'incomegroupcode',
        # 'project__recipient__income_group__display name': 'incomegroupname', #TODO: use diplay name
        'flow_type': 'flowcode',
        #'flow_type__display value': 'flowname', #TODO: use diplay name
        'bi_multi': 'bi_multi',
        'project__finance_type': 'finance_t',
        'project__aid_type': 'aid_t',
        'commitment_usd': 'usd_commitment',
        'disbursement_usd': 'usd_disbursement',
        # '': 'currencycode', #todo: aggiungerlo al csv
        'commitment': 'commitment_national',
        'disbursement': 'disbursement_national',
        # 'project__description': 'shortdescription', #char problem
        # 'project__title': 'projecttitle', #char problem
        'project__sector__code': 'purposecode',
        'project__sector__name': 'purposename',
        'project__sector__parent__code': 'sectorcode',
        'project__sector__parent__name': 'sectorname',
        'project__channel__code': 'channelcode',
        # 'project__channel__name': 'channelname', #todo: char problem
        # 'channel_reported__name': 'channelreportedname',#todo: char problem
        # 'geography': 'geography',#todo: char problem
        'expected_start_date': 'expectedstartdate',
        'completion_date': 'completiondate',
        'long_description': 'longdescription',
        'project__markers__gender': 'gender',
        'project__markers__environment': 'environment',
        'project__markers__trade': 'trade',
        'project__markers__pd_gg': 'pdgg',
        'is_ftc': 'FTC',
        'is_pba': 'PBA',
        'is_investment': 'investmentproject',
        'project__markers__biodiversity': 'biodiversity',
        'project__markers__climate_mitigation': 'climateMitigation',
        'project__markers__climate_adaptation': 'climateAdaptation',
        'project__markers__desertification': 'desertification',
        'commitment_date': 'commitmentdate',
        'number_repayment': 'numberrepayment',
        'grant_element': 'grantelement',
        'pk': 'openaid id',

    }

    csv_fieldset = {k:k for k in field_map.keys()}

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

        activity_set = activity_set.values(*self.csv_fieldset.keys())
        self.logger.info("Exported {} lines".format(len(activity_set)))
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
            self.logger.error("Command execution aborted.")
        finally:
            self.logger.info("Execution time: %d seconds" % (time.time() - start_time))
