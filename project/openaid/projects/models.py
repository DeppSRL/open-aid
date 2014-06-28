from django.db import models
from django.utils.translation import ugettext as _
from model_utils import Choices
from openaid import utils
from openaid.projects import fields


class ChannelReported(models.Model):

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Markers(models.Model):

    biodiversity = fields.MarkerField()
    climate_adaptation = fields.MarkerField()
    climate_mitigation = fields.MarkerField()
    desertification = fields.DesertificationMarkerField()
    environment = fields.MarkerField()
    gender = fields.MarkerField()
    pd_gg = fields.MarkerField()
    trade = fields.MarkerField()

    @property
    def names(self):
        return self._meta.get_all_field_names()

    def __unicode__(self):
        return ("{}"*8).format(*[getattr(self, name) or '-' for name in self.names])


class Project(models.Model):

    crsid = models.CharField(max_length=100, blank=True)
    recipient = models.ForeignKey('codelists.Recipient', blank=True, null=True)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField()

    def activities(self, year=None):
        if not getattr(self, '_activities', False):
            self._activities = list(self.activity_set.all().prefetch_related('recipient', 'agency', 'aid_type', 'channel', 'finance_type', 'sector'))
        return filter(lambda a: a.year == year, self._activities) if year else self._activities

    def _activities_map(self, field, activities=None, year=None):
        activities = activities or self.activities(year=year)
        return list(map(lambda a: getattr(a, field), activities)) if activities else []

    def years_range(self):
        return sorted(self._activities_map('year'))

    def title(self, year=None):
        titles = [a.title for a in self.activities(year)]
        if not any(titles):
            return ''
        title = titles[0]
        # prendo il titolo con piu caratteri
        for t in titles[1:]:
            if len(t) > len(title):
                title = t
        return title

    def description(self, year=None):
        descriptions = [a.description for a in self.activities(year)]
        if not any(descriptions):
            return ''
        description = descriptions[0]
        # prendo il titolo con piu caratteri
        for d in descriptions[1:]:
            if len(d) > len(description):
                description = d
        return description

    def recipients(self):
        return self._activities_map('aid_type')

    def agencies(self):
        return self._activities_map('agency')

    def aid_types(self):
        return self._activities_map('aid_type')

    def channels(self):
        return self._activities_map('channel')

    def finance_types(self):
        return self._activities_map('finance_type')

    def sectors(self):
        return self._activities_map('sector')

    def commitments(self, year=None):
        return self._activities_map('commitment', year=year)

    def commitment(self, year=None):
        return sum(self.usd_commitments(year=year or self.end_year), 0.0)

    def disbursements(self, year=None):
        return self._activities_map('disbursement')

    def disbursement(self, year):
        return sum(self.usd_disbursements(year=year or self.end_year), 0.0)

    class Meta:
        unique_together = (('crsid', 'recipient'),)


class Activity(models.Model):

    project = models.ForeignKey(Project, null=True, blank=True)

    crsid = models.CharField(max_length=100, blank=True)
    year = models.IntegerField()
    number = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    geography = models.CharField(max_length=100, blank=True)

    REPORT_TYPES = Choices(
        # prese da resources/crs/Codelist04042014.osd:Nature of submission
        (0, _('Unkwnon')),
        (1, _('New activity reported')),
        (2, _('Revision')),
        (3, _('Previously reported activity')), # increase/decrease of earlier commitment, disbursement on earlier commitment
        (5, _('Provisional data')),
        (8, _('Commitment = Disbursement')),
    )
    report_type = models.PositiveSmallIntegerField(_('Nature of submission'), choices=REPORT_TYPES)

    FLOW_TYPES = Choices(
        # prese da resources/crs/dsd.xml:CL_CRS1_FLOW
        (0, _('Unkwnon')),
        (11, _('ODA Grants')),
        (12, _('ODA Grant-Like')),
        (13, _('ODA Loans')),
        (14, _('Other Official Flows')), # (non Export Credit)
        (19, _('Equity Investment')),
        (30, _('Private Grants')),
        (100, _('Official Development Assistance')),
    )
    flow_type = models.PositiveSmallIntegerField(_('Flow type'), choices=FLOW_TYPES)

    BI_MULTI_TYPES = Choices(
        # prese da resources/crs/Codelist04042014.osd:Bi_Multi
        (0, _('Unknown')),
        (1, _('Bilateral')),
        (2, _('Multilateral')),
        (3, _('Bilateral, core contributions to NGOs and other private bodies / PPPs')),
        (7, _('Bilateral, ex-post reporting on NGOs\' activities funded through core contributions')),
        (4, _('Multilateral outflows')),
        (6, _('Private sector outflows')),
    )
    bi_multi = models.IntegerField(_('Bi/Multilateral'), choices=BI_MULTI_TYPES)

    is_ftc = models.BooleanField(_('Free Standing Technical Cooperation'), default=False)
    is_pba = models.BooleanField(_('Programme Based Approaches'), default=False)
    is_investment = models.BooleanField(_('Investment Project'), default=False)

    # money parameters
    commitment = models.FloatField(blank=True, null=True)
    commitment_usd = models.FloatField(blank=True, null=True)
    disbursement = models.FloatField(blank=True, null=True)
    disbursement_usd = models.FloatField(blank=True, null=True)

    # other parameters
    grant_element = models.FloatField(blank=True, null=True)
    number_repayment = models.PositiveIntegerField(blank=True, null=True)
    expected_start_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    commitment_date = models.DateTimeField(blank=True, null=True)

    # external relations
    markers = models.ForeignKey(Markers, null=True, blank=True)
    channel_reported = models.ForeignKey(ChannelReported, blank=True, null=True)

    recipient = models.ForeignKey('codelists.Recipient', null=True, blank=True)
    agency = models.ForeignKey('codelists.Agency', null=True, blank=True)
    aid_type = models.ForeignKey('codelists.AidType', null=True, blank=True)
    channel = models.ForeignKey('codelists.Channel', null=True, blank=True)
    finance_type = models.ForeignKey('codelists.FinanceType', null=True, blank=True)
    sector = models.ForeignKey('codelists.Sector', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.commitment and self.commitment_usd:
            self.commitment = utils.currency_converter(self.commitment_usd, self.year)
        if not self.disbursement and self.disbursement_usd:
            self.disbursement = utils.currency_converter(self.disbursement_usd, self.year)
        return super(Activity, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"{project}:{year}:{number}:{title}".format(year=self.year, project=self.project, number=self.number, title=self.title)

    class Meta:
        ordering = ('-year', 'number', 'title')
