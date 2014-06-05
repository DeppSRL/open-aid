import logging
from collections import defaultdict
from django.conf import settings
from django.forms.models import modelform_factory
import sdmx
from csvkit import DictReader
from openaid.crs import code_lists
from openaid.crs import forms
from openaid.crs import mapping
from openaid.crs import _models


__author__ = 'joke2k'


logger = logging.getLogger(__name__)

class CRSException(Exception):

    def __init__(self, invalid_form, *args, **kwargs):
        message = invalid_form.errors.as_text()
        Exception.__init__(self, message, *args, **kwargs)

class CRSRowException(CRSException):
    pass


def import_crs_file(csv_file, **kwargs):
    """
    Questa funzione si occupa di prendere le righe di un file csv,
    e passarle a import_csv_row per importare i progetti crs.
    """
    load_code_lists()
    logger.debug("Open csv dict reader with '%s' as csv data and with these kwargs: %s" % (csv_file.name, kwargs))
    rows = DictReader(csv_file, **kwargs)

    for i, row in enumerate(rows):

        yield import_crs_row(row)


def import_crs_row(row):
    """
    Questa funzione riceve un dict con i dati relativi
    ad una riga dei file csv sui CRS, e si occupa di mapparla
    nel modello django per salvarla nel database.
    """
    return ProjectRowLoader(row).load()

def load_code_lists():
    """
    Questa funzione carica le code list nel database
    """
    CodeListLoader().load()


class ProjectRowLoader(object):
    
    def __init__(self, row):
        self.row = row
        self.code_list_cache = {}

    def get_code_list_object(self, model, code):
        if model.code_list not in self.code_list_cache:
            self.code_list_cache[model.code_list] = {}
        if code not in self.code_list_cache[model.code_list]:
            self.code_list_cache[model.code_list][code] = model.objects.get(code=code)
        return self.code_list_cache[model.code_list][code]
        
    def load(self):
        # fix report_type
        if not self.row['initialreport']:
            self.row['initialreport'] = 0
        project_form = mapping.create_mapped_form(forms.ProjectForm, self.row, mapping.PROJECT_FIELDS_MAP)
    
        if not project_form.is_valid():
            raise CRSRowException(project_form)
    
        project = project_form.save(commit=False)

        # load CRS
        if self.row['crsid']:
            project.crs, _ = _models.CRS.objects.get_or_create(**mapping.convert_names(self.row, mapping.CRS_FIELDS_MAP))

        # load code lists values
        self.load_code_list_values(project)

        # load markers
        marker_form = mapping.create_mapped_form(forms.MarkerForm, self.row, mapping.MARKER_FIELDS_MAP)
        if not marker_form.is_valid():
            raise CRSRowException(marker_form)
        project.marker = marker_form.save()

        # load channel reported
        channel_reported_form = mapping.create_mapped_form(modelform_factory(_models.ChannelReported), self.row, mapping.CHANNEL_REPORTED_MAP)
        if channel_reported_form.is_valid():
            project.channel_reported, _ = _models.ChannelReported.objects.get_or_create(**channel_reported_form.cleaned_data)

        # save project with changes
        project.save()
    
        return project

    def load_code_list_values(self, project):
        # read code lists
        for code_list in _models.CODE_LIST_MODELS:

            form_class = modelform_factory(code_list)
            code_list_form = mapping.create_mapped_form(form_class, self.row, code_list.get_csv_fields_map())

            if code_list_form.is_valid():

                try:
                    code_list_object = self.get_code_list_object(code_list, code_list_form.cleaned_data['code'])
                    setattr(project, str(code_list.code_list_field), code_list_object)

                except code_list.DoesNotExist:
                    logging.warning('Invalid code "%s" for code list %s. valid values: %s' % (
                        code_list_form.cleaned_data['code'],
                        code_list,
                        code_list.objects.values_list('code', flat=True)
                    ))

                except code_list.MultipleObjectsReturned:
                    logging.warning('Multiple value with code "%s" in code list %s.' % (
                        code_list_form.cleaned_data['code'],
                        code_list
                    ))


class CodeListLoader(object):

    def __init__(self, dsd_file=settings.OPENAID_DSD_FILE):
        self.dsd = sdmx.dsd_reader(dsd_file)
        self.code_lists = _models.CODE_LIST_MODELS

    def load(self):
        for code_list in self.code_lists:
            if hasattr(self, 'load_%s' % code_list.code_list):
                getattr(self, 'load_%s' % code_list.code_list)(code_list)
            else:
                if hasattr(code_list, 'code_list_sdmx'):
                    self.load_code_list_from_dsd(code_list)
                else:
                    raise Exception('Cannot load code list "%s"' % code_list.code_list)

    def load_code_list_from_dsd(self, code_list):

        sdmx_code_list = self.dsd.code_list(code_list.code_list_sdmx)
        needs_parent = defaultdict(list)

        for code in sdmx_code_list.codes():

            params = {'code': code.value, 'name': code.description('en')}

            obj, created = code_list.objects.get_or_create(**params)

            if created and hasattr(obj, 'parent') and code.parent_code_id():
                needs_parent[code.parent_code_id()].append(obj.pk)

        if hasattr(code_list, 'parent'):
            # fill all parent to his children
            for parent in code_list.objects.filter(code__in=needs_parent.keys()):
                code_list.objects.filter(pk__in=needs_parent[parent.code]).update(parent=parent)

    def load_channel(self, code_list):
        needs_parent = defaultdict(list)

        for channel in code_lists.Channel.get_all():
            c, _ = _models.Channel.objects.get_or_create(
                code=channel.code,
                name=channel.name,
                # missing description here
            )
            if channel.parent:
                needs_parent[channel.parent.code].append(c.pk)

        for parent, children_pks in needs_parent.items():
            code_list.objects.filter(pk__in=children_pks).update(parent=parent)

    def load_finance_type(self, code_list):
        ft_groups = {}
        for finance_type in code_lists.FinanceGroup.get_all():
            ft_groups[finance_type.code], _ = _models.FinanceType.objects.get_or_create(
                code=finance_type.code,
                name=finance_type.name,
                # missing description here
                # and no parent for FinanceGroup
            )

        for finance_type in code_lists.FinanceType.get_all():
            _models.FinanceType.objects.get_or_create(
                code=finance_type.code,
                name=finance_type.name,
                parent=ft_groups[finance_type.group.code]
                # missing description here
            )

    def load_agency(self, code_list):
        for agency in code_lists.Agency.get_all_by_donor(settings.OPENAID_CRS_DONOR):
            _models.Agency.objects.get_or_create(
                code=agency.code,
                name=agency.name,
            )

    def load_sector(self, code_list):

        self.load_code_list_from_dsd(code_list)

        # then load purpose
        for sector in _models.Sector.objects.all():
            if sector.is_leaf_node():
                _models.Purpose.objects.create(
                    code=sector.code,
                    name=sector.name,
                )

    def load_purpose(self, code_list):
        # loaded in load_sector
        pass

    def load_recipient(self, code_list):
        for region in code_lists.Region.get_all():
            _models.Region.objects.create(
                code=region.code,
                name=region.name
            )

        for income_group in code_lists.IncomeGroup.get_all():
            _models.IncomeGroup.objects.create(
                code=income_group.code,
                name=income_group.name
            )

        for recipient in code_lists.Recipient.get_all():
            _models.Recipient.objects.create(
                code=recipient.code,
                name=recipient.name,
                income_group_id=recipient.income_group.code if recipient.income_group else None,
                region_id=recipient.region.code if recipient.region else None,
            )

    def load_incomegroup(self, code_list):
        # loaded in load_recipient
        pass

    def load_region(self, code_list):
        # loaded in load_recipient
        pass
