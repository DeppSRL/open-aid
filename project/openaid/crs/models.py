from django.db import models
from django.utils.translation import ugettext as _
from model_utils import Choices
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from openaid.crs import code_lists
from openaid.crs import fields


__author__ = 'joke2k'


class CodeListModel(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)

    @classmethod
    def get_csv_fields_map(cls):
        return {
            '%scode' % cls.code_list: 'code',
            '%sname' % cls.code_list: 'name',
        }

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<{0}:{1}> {2}".format(self.code_list, self.code, self.__unicode__())

    class Meta:
        abstract = True


class Recipient(MPTTModel, CodeListModel):

    code_list = 'recipient'
    # code_list_sdmx = 'CL_CRS1_DAC_RECIPIENT'

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    income_group = models.ForeignKey('crs.IncomeGroup', null=True, blank=True)
    region = models.ForeignKey('crs.Region', null=True, blank=True)

class IncomeGroup(CodeListModel):
    """
    Group of Recipients
    """
    code_list = 'incomegroup'
    code_list_field = 'income_group'

class Region(CodeListModel):
    code_list = 'region'

class Agency(CodeListModel):
    code_list = 'agency'

    acronym = models.CharField(max_length=50, blank=True)

class Flow(CodeListModel):
    """
    used to distinguish official development assistance,
    other official flows and private flows.
    """
    code_list = 'flow'
    code_list_sdmx = 'CL_CRS1_FLOW'

class Channel(MPTTModel, CodeListModel):
    """
    Channels of delivery.
    """
    code_list = 'channel'
    code_list_sdmx = 'CL_CRS1_CHANNEL'

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

class Sector(MPTTModel, CodeListModel):
    """

    """
    code_list = 'sector'
    code_list_sdmx = 'CL_CRS1_SECTOR'

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

class FinanceType(MPTTModel, CodeListModel):
    """
    Used to distinguish financial instruments, e.g. grants or loans.
    """
    code_list = 'finance_type'

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    @classmethod
    def get_csv_fields_map(cls):
        return {'finance_t': 'code'}

class AidType(MPTTModel, CodeListModel):
    """
    Used to distinguish aid modalities.
    """
    code_list = 'aid_type'
    code_list_sdmx = 'CL_CRS1_AIDTYPE'

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    @classmethod
    def get_csv_fields_map(cls):
        return {'aid_t': 'code'}

# Project models

class Project(models.Model):

    crs = models.CharField(max_length=100)
    recipient = models.ForeignKey(Recipient)

    def __unicode__(self):
        return "%s:%s" % (self.crs, self.recipient_id)

    class Meta:
        unique_together = ('crs', 'recipient')


class Markers(models.Model):

    biodiversity = fields.MarkerField()
    climate_adaptation = fields.MarkerField()
    climate_mitigation = fields.MarkerField()
    desertification = fields.DesertificationMarkerField()
    environment = fields.MarkerField()
    gender = fields.MarkerField()
    pd_gg = fields.MarkerField()
    trade = fields.MarkerField()

    names = ['biodiversity', 'climate_adaptation', 'climate_mitigation', 'desertification', 'environment', 'gender', 'pd_gg', 'trade']

    def __unicode__(self):
        return ("{}"*8).format(*[getattr(self, name) or '*' for name in self.names])


class ChannelReported(models.Model):

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Activity(models.Model):

    project = models.ForeignKey(Project, null=True, blank=True)
    markers = models.ForeignKey(Markers, null=True, blank=True)
    channel_reported = models.ForeignKey(ChannelReported, blank=True, null=True)

    agency = models.ForeignKey(Agency, null=True, blank=True)
    aid_type = models.ForeignKey(AidType, null=True, blank=True)
    finance_type = models.ForeignKey(FinanceType, null=True, blank=True)
    channel = models.ForeignKey(Channel, null=True, blank=True)
    purpose = models.ForeignKey(Sector, null=True, blank=True)
    flow = models.ForeignKey(Flow, null=True, blank=True)

    report_type = models.IntegerField('Nature of Submission', choices=Choices(
        # prese da resources/crs/Codelist04042014.osd:Nature of submission
        (0, _('Unkwnon')),
        (1, _('New activity reported')),
        (2, _('Revision')),
        (3, _('Previously reported activity')), # increase/decrease of earlier commitment, disbursement on earlier commitment
        (5, _('Provisional data')),
        (8, _('Commitment = Disbursement')),
    ))

    # project report parameters
    year = models.IntegerField()
    number = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    geography = models.CharField(max_length=100, blank=True)
    outflow = models.IntegerField('Bi/Multilateral', choices=Choices(
        # prese da resources/crs/Codelist04042014.osd:Bi_Multi
        (0, _('Unknown')),
        (1, _('Bilateral')),
        (2, _('Multilateral')),
        (3, _('Bilateral, core contributions to NGOs and other private bodies / PPPs')),
        (7, _('Bilateral, ex-post reporting on NGOs\' activities funded through core contributions')),
        (4, _('Multilateral outflows')),
        (6, _('Private sector outflows')),
    ))
    is_ftc = models.BooleanField(_('Free Standing Technical Cooperation'), default=False)
    is_pba = models.BooleanField(_('Programme Based Approaches'), default=False)
    is_investment = models.BooleanField(_('Investment Project'), default=False)

    # other parameters
    currency = models.IntegerField(choices=code_lists.DonorGroup.get_currency_choices('dac', 'non_dac'))
    commitment_national = models.FloatField(blank=True, null=True)
    disbursement_national = models.FloatField(blank=True, null=True)
    grant_element = models.FloatField(blank=True, null=True)
    number_repayment = models.PositiveIntegerField(blank=True, null=True)
    expected_start_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    commitment_date = models.DateTimeField(blank=True, null=True)

    # money parameters
    usd_commitment = models.FloatField(blank=True, null=True)
    usd_disbursement = models.FloatField(blank=True, null=True)

    usd_received = models.FloatField(blank=True, null=True)
    usd_commitment_defl = models.FloatField(blank=True, null=True)
    usd_disbursement_defl = models.FloatField(blank=True, null=True)
    usd_received_defl = models.FloatField(blank=True, null=True)
    usd_adjustment = models.FloatField(blank=True, null=True)
    usd_adjustment_defl = models.FloatField(blank=True, null=True)
    usd_amount_untied = models.FloatField(blank=True, null=True)
    usd_amount_partialtied = models.FloatField(blank=True, null=True)
    usd_amount_tied = models.FloatField(blank=True, null=True)
    usd_amount_untied_defl = models.FloatField(blank=True, null=True)
    usd_amount_partialtied_defl = models.FloatField(blank=True, null=True)
    usd_amount_tied_defl = models.FloatField(blank=True, null=True)
    usd_IRTC = models.FloatField(blank=True, null=True)
    usd_expert_commitment = models.FloatField(blank=True, null=True)
    usd_expert_extended = models.FloatField(blank=True, null=True)
    usd_export_credit = models.FloatField(blank=True, null=True)
    usd_interest = models.FloatField(blank=True, null=True)
    usd_outstanding = models.FloatField(blank=True, null=True)
    usd_arrears_principal = models.FloatField(blank=True, null=True)
    usd_arrears_interest = models.FloatField(blank=True, null=True)
    usd_future_DS_principal = models.FloatField(blank=True, null=True)
    usd_future_DS_interest = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return "{year}:{project}:{number}:{title}".format(year=self.year, project=self.project, number=self.number, title=self.title)


PROJECT_CODE_LIST_MODELS = [Recipient, IncomeGroup, Region]
ACTIVITY_CODE_LIST_MODELS = [Agency, Flow, Channel, Sector, AidType, FinanceType, ]
CODE_LIST_MODELS = PROJECT_CODE_LIST_MODELS + ACTIVITY_CODE_LIST_MODELS
