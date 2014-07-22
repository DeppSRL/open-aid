from django.contrib.contenttypes.generic import GenericRelation
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from model_utils import Choices
from openaid import utils
from openaid.projects import fields


class ChannelReported(models.Model):

    name = models.CharField(max_length=128)

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
        return ['biodiversity', 'climate_adaptation', 'climate_mitigation', 'desertification', 'environment', 'gender', 'pd_gg', 'trade']

    def __unicode__(self):
        return ("{}"*8).format(*[getattr(self, name) or '-' for name in self.names])


class Project(models.Model):

    crsid = models.CharField(max_length=128, blank=True)
    recipient = models.ForeignKey('codelists.Recipient', blank=True, null=True)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField()
    has_focus = models.BooleanField(_('Focus'), default=False)
    photo_set = GenericRelation('attachments.Photo')

    @classmethod
    def get_top_projects(cls, qnt=3, order_by=None, year=None, **filters):
        if year:
            filters['year'] = year
        projects = Activity.objects.filter(**filters).order_by('project').distinct('project').values('project', 'commitment')
        def order_by_commitment(project):
            return -1 * ( project.get('commitment') or 0)
        projects = sorted(projects, key=order_by or order_by_commitment)[:qnt]
        return cls.objects.filter(pk__in=map(lambda p: p.get('project'), projects))

    def related_projects(self, qnt=3):
        return Project.objects.all().order_by('?')[:qnt]

    def activities(self, year=None):
        if not getattr(self, '_activities', False):
            self._activities = list(self.activity_set.all().prefetch_related('recipient', 'agency', 'aid_type', 'channel', 'finance_type', 'sector'))
        return filter(lambda a: a.year == year, self._activities) if year else self._activities

    def _activities_map(self, field, activities=None, year=None, skip_none=False):
        activities = activities or self.activities(year=year)
        activities = list(map(lambda a: getattr(a, field), activities)) if activities else []
        if skip_none:
            activities = filter(lambda a: a is not None, activities)
        return activities

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
            descriptions = [a.long_description for a in self.activities(year)]
            if not any(descriptions):
                return ''
        description = descriptions[0]
        # prendo il titolo con piu caratteri
        for d in descriptions[1:]:
            if len(d) > len(description):
                description = d
        return description

    def recipients(self):
        return self._activities_map('recipient')

    def agencies(self, year=None):
        return self._activities_map('agency', year=year)

    def agency(self, year=None):
        return self.agencies(year=year)[0]

    def aid_types(self):
        return self._activities_map('aid_type', skip_none=True)

    def channels(self):
        return self._activities_map('channel', skip_none=True)

    def finance_types(self):
        return self._activities_map('finance_type', skip_none=True)

    def sectors(self):
        return self._activities_map('sector', skip_none=True)

    def purpose(self, year=None):
        return self._activities_map('sector', year=None, skip_none=True)[0]

    def channel_reported(self, year=None):
        return self._activities_map('channel_reported', year=year)[0]

    def commitments(self, year=None):
        return self._activities_map('commitment', year=year)

    def commitment(self, year=None):
        return sum(self._activities_map('commitment', year=year or self.end_year, skip_none=True), 0.0)

    def total_commitment(self):
        return sum(self._activities_map('commitment', skip_none=True), 0.0)

    def disbursements(self, year=None):
        return self._activities_map('disbursement')

    def disbursement(self, year=None):
        return sum(self._activities_map('disbursement', year=year or self.end_year, skip_none=True), 0.0)

    def total_disbursement(self):
        return sum(self._activities_map('disbursement', skip_none=True), 0.0)

    def flow_type(self, year=None):
        for a in self.activities(year=year):
            return a.get_flow_type_display()
        return None

    def bi_multi(self, year=None):
        for a in self.activities(year=year):
            return a.get_bi_multi_display()
        return None

    def finance_type(self, year=None):
        return self._activities_map('finance_type', year=year, skip_none=True)[0]

    def completion_date(self, year=None):
        dates = self._activities_map('completion_date', year=year, skip_none=True)
        return dates[0] if dates else None

    def expected_start_date(self, year=None):
        dates = self._activities_map('expected_start_date', year=year, skip_none=True)
        return dates[0] if dates else None

    def is_ftc(self, year=None):
        return any(self._activities_map('is_ftc', year=year))

    def is_pba(self, year=None):
        return any(self._activities_map('is_pba', year=year))

    def is_investment(self, year=None):
        return any(self._activities_map('is_investment', year=year))

    def get_absolute_url(self):
        return reverse('projects:project-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return "Project:%s:%s" % (self.crsid, self.recipient)

    class Meta:
        unique_together = (('crsid', 'recipient'),)


class Activity(models.Model):

    project = models.ForeignKey(Project, null=True, blank=True)

    crsid = models.CharField(max_length=128, blank=True)
    year = models.IntegerField()
    number = models.CharField(max_length=128, blank=True)
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    geography = models.CharField(max_length=128, blank=True)

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
        return u"{project}:{year}".format(year=self.year, project=self.project)

    class Meta:
        ordering = ('-year', 'number', 'title')


class Organization(models.Model):
    """
    Organizzazioni a cui vanno i fondi multilaterali.
    I Projects sono relativi ai fondi bilaterali.
    """
    code = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class AnnualFunds(models.Model):
    """
    Rappresenta i fondi multilaterali anno per anno delle Organization.
    """
    year = models.PositiveSmallIntegerField()
    organization = models.ForeignKey(Organization)

    commitment = models.FloatField(blank=True, default=0.0)
    disbursement = models.FloatField(blank=True, default=0.0)

    def __unicode__(self):
        return '%s %s: %f/%f' % (self.organization, self.year, self.commitment, self.disbursement)

    class Meta:
        unique_together = ("year", "organization")