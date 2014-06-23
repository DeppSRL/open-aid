"""
Produce un piu csv uno per code list
dove ogni riga presenta
Project.crs:Project.recipient_id
e il valore anno dopo anno di quella code list.

CRSID | RECIPIENT | 2004 | ... | 2012

"""
import csv

from openaid.crs.models import Project

YEARS = [str(x) for x in range(2004, 2013)]
DEFAULT_YEARS_VALUES = dict([(y, u'') for y in YEARS])
FIELDS = ['crsid', 'recipient', ] + [str(x) for x in range(2004, 2013)]

def create_writer(name):
    f = open('%s.csv' % name, 'w')
    return f, csv.DictWriter(f, FIELDS)


def run():

    aid_file, aid_writer = create_writer('aid')
    aid_writer.writeheader()
    sector_file, sector_writer = create_writer('sector')
    sector_writer.writeheader()
    channel_file, channel_writer = create_writer('channel')
    channel_writer.writeheader()

    for i, project in enumerate(Project.objects.all()):

        aids = {}
        sectors = {}
        channels = {}

        for activity in project.activity_set.all():

            year = str(activity.year)

            aids[year] = activity.aid_type.code if activity.aid_type else ''
            sectors[year] = activity.purpose.code if activity.purpose else ''
            channels[year] = activity.channel.code if activity.channel else ''

        line = {
            'crsid': project.crs,
            'recipient': project.recipient.code,
        }
        line.update(DEFAULT_YEARS_VALUES)

        for codelist, writer in [(aids, aid_writer), (sectors, sector_writer), (channels, channel_writer)]:

            codelist_line = line.copy()
            codelist_line.update(codelist)
            writer.writerow(codelist_line)

    aid_file.close()
    sector_file.close()
    channel_file.close()