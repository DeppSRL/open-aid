# coding=utf-8
from __future__ import unicode_literals
import csvkit
from openaid.codelists.models import Agency
from openaid.projects.models import Activity

__author__ = 'joke2k'

DGCS = '4'
Artigiancassa = '9'
Ministero = '7'
Comune = '8'
University = '7'





TIPI = [
    "Agency Artigiancassa",
    "Agency Comune",
    "Agency Ministero",
    "Agency Università",
    "DGCS projnumb",
    "DGCS projnumb, aid t e channel",
    "DGCSvuoto",
]


def run():

    agencies = dict(Agency.objects.values_list('code', 'pk'))


    for row in csvkit.DictReader(open('dgcs_fixes.csv')):

        if row['tipologia'] not in TIPI:
            raise Exception("%s not in %s" % (row['tipologia'], TIPI))

        updater = Activity.objects.filter(agency__code=DGCS, crsid=row['crsid'])

        if row['tipologia'] == "Agency Artigiancassa":
            print 'update to Artigiancassa: %s to %s' % (updater.values_list('agency__code', flat=True), agencies[Artigiancassa] ),
            print updater.update(agency=agencies[Artigiancassa])

        elif row['tipologia'] == "Agency Comune":
            print 'update to Comune: %s to %s' % (updater.values_list('agency__code', flat=True), agencies[Comune] ),
            print updater.update(agency=agencies[Comune])

        elif row['tipologia'] == "Agency Ministero":
            print 'update to Ministero: %s to %s' % (updater.values_list('agency__code', flat=True), agencies[Ministero] ),
            print updater.update(agency=agencies[Ministero])

        elif row['tipologia'] == "Agency Università":
            print 'update to Universita: %s to %s' % (updater.values_list('agency__code', flat=True), agencies[University] ),
            print updater.update(agency=agencies[University])

        elif row['tipologia'].startswith('DGCS projnumb'):
            print 'update to project number: %s to %s' % (updater.values_list('number', flat=True), row['projectnumber_ok'] ),
            print updater.update(number=row['projectnumber_ok'])

