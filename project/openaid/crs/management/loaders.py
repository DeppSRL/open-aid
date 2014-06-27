# coding=utf-8
from collections import defaultdict
import logging
from django.conf import settings
from django.forms.models import modelform_factory
import csvkit
import sdmx
from openaid.crs import utils
from openaid.crs import code_lists
from openaid.crs import forms
from openaid.crs import mapping
from openaid.crs import models
from openaid.crs.forms import text_cleaner

__author__ = 'joke2k'

logger = logging.getLogger(__name__)


class CRSException(Exception):

    def __init__(self, invalid_form, *args, **kwargs):
        message = invalid_form.errors.as_text()
        Exception.__init__(self, message, *args, **kwargs)


class CodeListLoader(object):

    def __init__(self, dsd_file=settings.OPENAID_DSD_FILE):
        self.dsd = sdmx.dsd_reader(dsd_file)
        self.code_lists = models.CODE_LIST_MODELS

    def load(self):
        logger.debug('Start loading code lists')
        for code_list in self.code_lists:
            logger.debug('Code list: %s' % code_list)
            if hasattr(self, 'load_%s' % code_list.code_list):
                getattr(self, 'load_%s' % code_list.code_list)(code_list)
            else:
                if hasattr(code_list, 'code_list_sdmx'):
                    self.load_code_list_from_dsd(code_list)
                else:
                    raise Exception('Cannot load code list "%s"' % code_list.code_list)

    def load_code_list_from_dsd(self, code_list):

        sdmx_code_list = self.dsd.code_list(code_list.code_list_sdmx)
        is_hierarchy = hasattr(code_list, 'parent')
        # needs_parent = defaultdict(list)
        parents = {}
        bans = getattr(code_list, 'code_list_excludes', [])

        for code in sdmx_code_list.codes():

            params = {'code': code.value, 'name': code.description('en')}
            defaults = {}

            if code.value in bans or code.parent_code_id() in bans or (code.parent_code_id() in parents and parents[code.parent_code_id()].code in bans):
                continue

            if is_hierarchy:
                defaults = {'parent': parents.get(code.parent_code_id()) if code.parent_code_id() else None}

            obj, created = code_list.objects.get_or_create(defaults=defaults, **params)

            if created:
                if is_hierarchy:
                    parents[code.value] = obj
                # if is_hierarchy and code.parent_code_id():
                #     needs_parent[code.parent_code_id()].append(obj.pk)

        # if hasattr(code_list, 'parent'):
        #     # fill all parent to his children
        #     for parent in code_list.objects.filter(code__in=needs_parent.keys()):
        #         code_list.objects.filter(pk__in=needs_parent[parent.code]).update(parent=parent)

    def load_channel(self, code_list):
        # needs_parent = defaultdict(list)
        channels = {}
        for channel in code_lists.Channel.get_all():
            defaults = {
                'parent': channels[channel.parent.code] if channel.parent else None,
            }
            channel_object, created = models.Channel.objects.get_or_create(
                code=channel.code,
                name=channel.name,
                defaults=defaults
            )
            channels[channel.code] = channel_object

            # if channel.parent:
                #needs_parent[channel.parent.code].append(c.pk)

        # for parent, children_pks in needs_parent.items():
        #     code_list.objects.filter(pk__in=children_pks).update(parent=parent)

    def load_finance_type(self, code_list):
        ft_groups = {}
        for finance_type in code_lists.FinanceGroup.get_all():
            ft_groups[finance_type.code], _ = models.FinanceType.objects.get_or_create(
                code=finance_type.code,
                name=finance_type.name,
                # missing description here
                # and no parent for FinanceGroup
            )

        for finance_type in code_lists.FinanceType.get_all():
            models.FinanceType.objects.get_or_create(
                code=finance_type.code,
                name=finance_type.name,
                parent=ft_groups[finance_type.group.code]
                # missing description here
            )

    def load_agency(self, code_list):
        for agency in code_lists.Agency.get_all_by_donor(settings.OPENAID_CRS_DONOR):
            models.Agency.objects.get_or_create(
                code=agency.code,
                name=agency.name,
                acronym=agency.acronym
            )

    def load_recipient(self, code_list):
        regions = {}
        for region in code_lists.Region.get_all():
            region_object, created = models.Region.objects.get_or_create(
                code=region.code,
                name=region.name
            )
            regions[region.code] = region_object

        income_groups = {}
        for income_group in code_lists.IncomeGroup.get_all():
            income_group_object, created = models.IncomeGroup.objects.get_or_create(
                code=income_group.code,
                name=income_group.name
            )
            income_groups[income_group.code] = income_group_object

        for recipient in code_lists.Recipient.get_all():
            models.Recipient.objects.get_or_create(
                code=recipient.code,
                name=recipient.name,
                income_group_id=income_groups[recipient.income_group.code].pk if recipient.income_group else None,
                region_id=regions[recipient.region.code].pk if recipient.region else None,
            )

    def load_incomegroup(self, code_list):
        # loaded in load_recipient
        pass

    def load_region(self, code_list):
        # loaded in load_recipient
        pass


class CRSFileLoader(object):

    def __init__(self, csv_file, **options):
        self.csv_file = csv_file
        self.options = options

    def load(self):
        """
        Questa funzione si occupa di prendere le righe di un file csv,
        e passarle a import_csv_row per importare i progetti crs.
        """
        CodeListLoader().load()
        logger.debug("Open csv dict reader with '%s' as csv data and with these kwargs: %s" % (self.csv_file.name, self.options))
        rows = csvkit.DictReader(self.csv_file, **self.options)

        for i, row in enumerate(rows):

            yield ActivityRowLoader(row).load()

class ActivityRowLoader(object):

    def __init__(self, row):
        self.row = row
        self.code_list_cache = {}

    def get_code_list_object(self, model, code):
        if model.code_list not in self.code_list_cache:
            self.code_list_cache[model.code_list] = {}
        if code not in self.code_list_cache[model.code_list]:
            try:
                self.code_list_cache[model.code_list][code] = model.objects.get(code=code)
            except model.DoesNotExist:
                raise Exception("Cannot retrieve %s with code '%s'" % (model, code))
        return self.code_list_cache[model.code_list][code]

    def load(self):
        # fix report_type
        if not self.row['initialreport']:
            self.row['initialreport'] = 0
        # fix empty flow
        if self.row['flowcode'] == '99' and self.row['flowname'] == '':
            self.row['flowcode'] = ''

        # 1. creo l'Activity
        activity_form = mapping.create_mapped_form(forms.ActivityForm, self.row, mapping.ACTIVITY_FIELDS_MAP)
        if not activity_form.is_valid():
            raise CRSException(activity_form)
        utils.currency_converter(activity_form.instance)
        activity = activity_form.save()

        # 2. vedo se può essere associata ad un Project
        if self.row['crsid'] and self.row['recipientcode']:
            project, created = models.Project.objects.get_or_create(**{
                'crs': self.row['crsid'],
                'recipient': self.get_code_list_object(models.Recipient, self.row['recipientcode']),
            })
            if not created:
                # logger.debug('New activity for project')
                pass
            activity.project = project
            activity.save() ## posso farlo dopo?

         # 3. creo i markers e i channel reported
        markers_form = mapping.create_mapped_form(forms.MarkersForm, self.row, mapping.MARKERS_FIELDS_MAP)
        if markers_form.is_valid():
            activity.markers = markers_form.save()

        # 4. associo il channel reported
        channel_reported_form = mapping.create_mapped_form(modelform_factory(models.ChannelReported), self.row, mapping.CHANNEL_REPORTED_MAP)
        if channel_reported_form.is_valid():
            crn, _ = models.ChannelReported.objects.get_or_create(name=channel_reported_form.instance.name)
            activity.channel_reported = crn

        # 5. aggiungo le code lists
        self.load_code_list_values(activity)

        # save project with changes
        activity.save()

        return activity

    def load_code_list_values(self, activity):
        # read code lists
        for code_list in models.ACTIVITY_CODE_LIST_MODELS:

            form_class = modelform_factory(code_list)
            code_list_form = mapping.create_mapped_form(form_class, self.row, code_list.get_csv_fields_map())

            if code_list_form.is_valid():
                try:

                    code_list_object = self.get_code_list_object(code_list, code_list_form.cleaned_data['code'])

                    if code_list is models.Sector:

                        purpose_form = modelform_factory(models.Sector)({'code': self.row['purposecode'], 'name': self.row['purposename']})
                        if not purpose_form.is_valid():
                            raise CRSException(purpose_form)
                        purpose_object = self.get_code_list_object(models.Sector, purpose_form.cleaned_data['code'])
                        if code_list_object not in purpose_object.get_ancestors(include_self=True):
                            raise Exception("Invalid purpose code '%s': it not matches with sector code '%s' [%s]" % (purpose_form.cleaned_data['code'], code_list_form.cleaned_data['code'], purpose_object.get_ancestors()))
                        setattr(activity, 'purpose', purpose_object)
                    else:
                        setattr(activity, code_list.code_list_field if hasattr(code_list, 'code_list_field') else code_list.code_list, code_list_object)

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
            else:
                if code_list_form.data['code']:
                    logger.warning("""
                    Activity: %s
                    Code list: %s
                    Form data: %s
                    Errors: %s
                    ROW: %s
                    """ % (activity, code_list, mapping.convert_names(self.row, code_list.get_csv_fields_map()), code_list_form.errors.as_text(), self.row))

class ActivityTranslator(object):

    def __init__(self, csv_file, field, **options):
        self.csv_file = csv_file
        self.field = field
        self.options = options

    def translate(self):
        rows = csvkit.DictReader(self.csv_file, **self.options)
        languages = [lang[0].split('-')[0] for lang in settings.LANGUAGES]
        for i, row in enumerate(rows):

            field_value = text_cleaner(row[self.field])
            if field_value == '':
                continue

            translations ={}
            for lang in languages:

                translated_field = '%s_%s' % (self.field, lang)

                if translated_field not in row.keys():
                    continue

                translations[translated_field] = text_cleaner(row[translated_field] or field_value)

            updates = models.Activity.objects.filter(**{
                '%s__iexact' % self.field: field_value
            }).update(**translations)

            yield field_value, updates
