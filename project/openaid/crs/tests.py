import os
import io
from django.conf import settings
from django.test import TestCase
from openaid.crs import code_lists
from openaid.crs import models
from openaid.crs import mapping
from openaid.crs.management import loaders
import sdmx

SAMPLE_FILE = os.path.join(settings.RESOURCES_DIR, 'crs', 'crs.sample.csv')
SAMPLE_FILE_ENCODING = 'utf-8'
def file_len(filename):
    i = 0
    with io.open(filename, 'r', encoding=SAMPLE_FILE_ENCODING) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
SAMPLE_FILE_LEN = file_len(SAMPLE_FILE) -1 # the number of sample projects, header exclude


class CRSTest(TestCase):

    def model_mapping_fields(self, model, names_map):
        # testo se ogni campo mappato ha il suo corrispondente nei fields del csv
        # e nei campi del modello
        for csv_field, model_field in names_map.items():
            self.assertIn(csv_field, mapping.ALL_FIELDS)
            self.assertIn(model_field, model._meta.get_all_field_names())

class MappingTest(CRSTest):

    def test_all_fields(self):
        self.assertEqual(80, len(mapping.ALL_FIELDS))

    def test_excluded_fields(self):
        for field in mapping.EXCLUDED_FIELDS:
            self.assertIn(field, mapping.ALL_FIELDS)

    def test_parsable_fields(self):
        for field in mapping.PARSABLE_FIELDS:
            self.assertIn(field, mapping.ALL_FIELDS)

    def test_convert_names(self):
        test_data = dict(foo=1)
        self.assertEqual(test_data, mapping.convert_names(test_data, {'foo': 'foo'}))
        self.assertEqual(dict(bar=1), mapping.convert_names(test_data, {'foo': 'bar'}))

    def test_create_mapped_form(self):
        names_map = {'foo': 'bar'}
        data = {'foo': 1}
        kwargs = {'opt': True}

        class Form(object):
            def __init__(self, data, **kwargs):
                self.data = data
                self.kwargs = kwargs

        form_instance = mapping.create_mapped_form(Form, data, names_map, **kwargs)
        self.assertTrue(form_instance)
        self.assertEqual(form_instance.__class__, Form)
        self.assertEqual(form_instance.data, mapping.convert_names(data, names_map))


class ModelMappingTest(CRSTest):

    def test_project_mapping_fields(self):
        self.model_mapping_fields(models.Project, mapping.PROJECT_FIELDS_MAP)

    def test_activity_mapping_fields(self):
        self.model_mapping_fields(models.Activity, mapping.ACTIVITY_FIELDS_MAP)

    def test_markers_mapping_fields(self):
        self.model_mapping_fields(models.Markers, mapping.MARKERS_FIELDS_MAP)

    def test_code_list_mapping_csv_fields(self):
        for code_list_model in models.CODE_LIST_MODELS:
            self.model_mapping_fields(code_list_model, code_list_model.get_csv_fields_map())

    def test_that_all_fields_is_mapped(self):
        mapped_fields = {}

        mapped_fields.update(mapping.PROJECT_FIELDS_MAP)
        mapped_fields.update(mapping.ACTIVITY_FIELDS_MAP)
        for code_list in models.CODE_LIST_MODELS:
            mapped_fields.update(code_list.get_csv_fields_map())
        mapped_fields.update(mapping.CHANNEL_REPORTED_MAP)
        mapped_fields.update(mapping.MARKERS_FIELDS_MAP)

        for csv_field, model_field in mapped_fields.items():
            self.assertIn(csv_field, mapping.PARSABLE_FIELDS)

        # remove purpose because it is a sector
        # parsable_fields = filter(lambda x: not x.startswith('purpose') and not x.startswith('region') and not x.startswith('incomegroup'), mapping.PARSABLE_FIELDS)
        parsable_fields = filter(lambda x: not x.startswith('purpose') , mapping.PARSABLE_FIELDS)

        self.assertEqual(sorted(mapped_fields.keys()), sorted(parsable_fields))

class ImportCRSTest(CRSTest):

    def test_import_code_lists(self):
        loaders.CodeListLoader().load()

        # recipients_count = len(code_lists.Recipient.get_all())
        # self.assertEqual(models.Recipient.objects.count(), recipients_count)

        # test agencies
        agencies_count = len(code_lists.Agency.get_all_by_donor(settings.OPENAID_CRS_DONOR))
        self.assertTrue(agencies_count)
        self.assertEqual(models.Agency.objects.count(), agencies_count)

        dsd = sdmx.dsd_reader(settings.OPENAID_DSD_FILE)

        # test flows
        flows_count = len(dsd.code_list(models.Flow.code_list_sdmx).codes())
        self.assertEqual(models.Flow.objects.count(), flows_count)

        # test channels
        channels_count = len(code_lists.Channel.get_all())
        self.assertEqual(models.Channel.objects.count(), channels_count)

        # test sectors
        sectors_count = len(dsd.code_list(models.Sector.code_list_sdmx).codes())
        self.assertEqual(models.Sector.objects.count(), sectors_count)

        # test purposes ( last level of sectors )
        # purposes_count = len([sector for sector in models.Sector.objects.all() if sector.is_leaf_node()])
        # self.assertEqual(models.Sector.objects.count(), purposes_count)

        # # test incomegroups
        # incomegroups_count = len(code_lists.IncomeGroup.get_all())
        # self.assertEqual(models.IncomeGroup.objects.count(), incomegroups_count)
        #
        # # test regions
        # regions_count = len(code_lists.Region.get_all())
        # self.assertEqual(models.Region.objects.count(), regions_count)

        # test aid_types
        aid_types = len(dsd.code_list(models.AidType.code_list_sdmx).codes())
        self.assertEqual(models.AidType.objects.count(), aid_types)

        # test finance_types
        finance_types_count = len(code_lists.FinanceGroup.get_all()) + len(code_lists.FinanceType.get_all())
        self.assertEqual(models.FinanceType.objects.count(), finance_types_count)


    def test_import_projects_from_csv(self):
        i = 0
        with io.open(SAMPLE_FILE, 'r', encoding=SAMPLE_FILE_ENCODING) as crs_file:
            for i, activity in enumerate(loaders.CRSFileLoader(crs_file).load(), start=1):
                self.assertTrue(activity.pk)
        self.assertEqual(i, SAMPLE_FILE_LEN)

