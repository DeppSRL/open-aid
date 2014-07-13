# coding=utf-8
from optparse import make_option
import csvkit
from os.path import join
from django.conf import settings
from django.core.management.base import CommandError, BaseCommand
from openaid.projects import models



class Command(BaseCommand):
    args = '<crs_file crs_file ...>'
    help = 'Importa le informazioni sui fondi multilaterali (resources/crs/organizations.csv)'

    option_list = BaseCommand.option_list + (
        make_option(
            "-f",
            "--file",
            dest = "organizations",
            help = "specify import file",
            metavar = "FILE",
            default=join(settings.RESOURCES_PATH, 'multilateral/organizations.csv'),
        ),
        make_option(
            "--funds",
            dest = "funds",
            help = "specify funds import file",
            metavar = "FILE",
            default=join(settings.RESOURCES_PATH, 'multilateral/funds.csv'),
        ),
        make_option('-c', '--clean',
            action='store_true', dest='clean', default=False,
            help="Clean old organizations and annual funds before executing the import."),
        make_option('-o', '--override',
            action='store_true', dest='override',
            help="Override old values."),
    )

    def delete_organizations(self):
        answer = raw_input('Are you sure? (Yes/No)')
        if answer.lower() in ('yes', 'y'):
            self.stdout.write('Deleting %s annual funds' % models.AnnualFunds.objects.count())
            models.AnnualFunds.objects.all().delete()
            self.stdout.write('Deleting %s organizations' % models.Organization.objects.count())
            models.Organization.objects.all().delete()
            return True
        return False

    def handle(self, *args, **options):

        self.stdout.write('Import organizations and annual funds')

        if options.get('clean') and not self.delete_organizations():
            raise CommandError("Import aborted")

        orgs = {}

        for row in csvkit.DictReader(open(options['organizations'])):

            org, created = models.Organization.objects.get_or_create(code=row['code'], name=row['name'])
            if created:
                self.stdout.write('Create new organization: %s' % org)
            else:
                self.stdout.write('Already created organization: %s' % org)
            orgs[org.code] = org

        for row in csvkit.DictReader(open(options['funds'])):

            commitment = float(row['commitment'].replace(',', '.') or 0.0)
            disbursement = float(row['disbursement'].replace(',', '.') or 0.0)

            fund, created = models.AnnualFunds.objects.get_or_create(
                organization=orgs[row['organization']],
                year=row['year'],
                defaults={
                    'commitment': commitment,
                    'disbursement': disbursement,
                }
            )
            if created:
                self.stdout.write('Add fund for %s' % fund)
            elif options['override']:
                to_save = False
                if fund.commitment != commitment:
                    self.stdout.write('Update fund commitment %s for %s' % (commitment, fund))
                    fund.commitment = commitment
                    to_save = True
                if fund.disbursement != disbursement:
                    self.stdout.write('Update fund disbursement %s for %s' % (disbursement, fund))
                    fund.disbursement = disbursement
                    to_save = True

                if to_save:
                    fund.save()
                    self.stdout.write('Updated fund for %s' % fund)
