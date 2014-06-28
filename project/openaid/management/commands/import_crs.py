# coding=utf-8
from optparse import make_option
import time
import csvkit
from django.core.management.base import LabelCommand, CommandError
from openaid.codelists import models as codelist_models
from openaid.projects import models
from openaid.projects import forms
from openaid.projects import mapping



class Command(LabelCommand):
    args = '<crs_file crs_file ...>'
    help = 'Speficica i CRS file da lavorare'

    option_list = LabelCommand.option_list + (
        make_option('-c', '--clean',
            action='store_true', dest='clean', default=False,
            help="Clean old activities and projects before import crs file."),
    )

    def delete_code_lists(self):
        answer = raw_input('Are you sure? (Yes/No)')
        if answer.lower() in ('yes', 'y'):
            self.stdout.write('Deleting %s projects' % models.Project.objects.count())
            models.Project.objects.all().delete()
            self.stdout.write('Deleting %s activities' % models.Activity.objects.count())
            models.Activity.objects.all().delete()
            return True
        return False

    def handle_label(self, crs_filename, **options):
        """
        Gli argomenti forniti sono i nomi dei file CRS da lavorare
        """
        start_time = time.time()
        i = 0

        if options.get('clean') and not self.delete_code_lists():
            raise CommandError("Import aborted")

        self.all_codelists = dict([
            (cl.code_list, dict(cl.objects.values_list('code', 'pk')))
            for cl in codelist_models.CODE_LISTS
        ])

        rows = 0
        with open(crs_filename, 'r') as crs_file:
            i = 0
            for rows, activity in enumerate(csvkit.DictReader(crs_file), start=1):
                if self.load_activity(activity, i):
                    i += 1
                    self.stdout.write("\rImported project: %d" % (i), ending='')
                    self.stdout.flush()


        self.stdout.write("\nTotal rows: %d" % rows)
        self.stdout.write("Execution time: %d seconds" % (time.time() - start_time))

    def load_activity(self, row, i):
        # fix report_type
        if not row['initialreport']:
            row['initialreport'] = 0
        # fix empty flow
        if row['flowcode'] == '' or (row['flowcode'] == '99' and row['flowname'] == ''):
            row['flowcode'] = 0

        # 1. creo l'Activity
        activity_form = mapping.create_mapped_form(forms.ActivityForm, row, mapping.ACTIVITY_FIELDS_MAP)
        if not activity_form.is_valid():
            self.stderr.write('\nError on row %s:\n%s' % (i, activity_form.errors.as_text()))
            return
        activity = activity_form.save()

         # 2. creo i markers
        markers_form = mapping.create_mapped_form(forms.MarkersForm, row, mapping.MARKERS_FIELDS_MAP)
        if markers_form.is_valid():
            activity.markers = markers_form.save()

        # 3. associo il channel reported
        channel_reported_form = mapping.create_mapped_form(forms.ChannelReportedForm, row, mapping.CHANNEL_REPORTED_MAP)
        if channel_reported_form.is_valid():
            crn, _ = models.ChannelReported.objects.get_or_create(name=channel_reported_form.instance.name)
            activity.channel_reported = crn

        # 4. aggiungo le code lists
        for codelist in codelist_models.CODE_LISTS:
            code_field = getattr(codelist, 'code_list_csv_field', False) or '%scode' % codelist.code_list
            code_value = row[code_field]
            if code_value:
                try:
                    pk = self.all_codelists[codelist.code_list][code_value]
                    setattr(activity, '%s_id' % codelist.code_list, pk)
                except KeyError:
                    self.stderr.write('\nError: cannot find %s with code "%s" (row: %s)' % (codelist.code_list, code_value, i))
        # save project with changes
        activity.save()

        return activity
