from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum, get_model
from django.utils.translation import ugettext as _
from model_utils import Choices
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from tinymce import models as tinymce_models

#### ABSTRACT CLASSES


class CodeListModel(models.Model):
    code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=512, blank=True)
    description = tinymce_models.HTMLField(blank=True)

    code_list = ''

    @property
    def code_list_facet(self):
        return self.code_list + 's'

    def top_projects(self, qnt=settings.TOP_ELEMENTS_NUMBER, order_by=None, year=None):
        return get_model('projects', 'Project').get_top_projects(qnt=qnt, order_by=order_by, year=year, **{
            '%s_id__in' % self.code_list: self.get_descendants_pks(True)
        })

    def top_initiatives(self, year=None):
        codelist_complete_set = self.get_descendants_pks(True)
        # filters top initiatives for recipient / sector if needed.
        # todo: change this when initiative OBJ changes field names!
        filters = {}
        if self.code_list == 'recipient':
            filters = {'recipient_temp__in': codelist_complete_set}
        elif self.code_list == 'sector':
            filters = {'purpose_temp__in': codelist_complete_set}

        return get_model('projects', 'Initiative').get_top_initiatives(year=year, **filters)

    def get_descendants_pks(self, include_self=False):
        return [self, ] if include_self else []

    def get_total(self, field, **filters):

        assert field in ('commitment', 'disbursement')

        filters.update({
            '%s__in' % getattr(self, 'code_list_activity_field', self.code_list): self.get_descendants_pks(True),
        })
        total = self.activity_set.model.objects.filter(**filters).aggregate(tot=Sum(field))['tot'] or 0.0
        return total

    def get_total_commitment(self, **filters):
        return self.get_total('commitment', **filters)

    def get_total_disbursement(self, **filters):
        return self.get_total('disbursement', **filters)

    def get_absolute_url(self):
        return reverse('codelists:%s-detail' % self.code_list, kwargs={'code': self.code})

    def __unicode__(self):
        return '[%s] %s' % (self.code, self.name_en)

    def __repr__(self):
        return u"<{0}:{1}> {2}".format(self.code_list, self.code, self.__unicode__())

    class Meta:
        abstract = True
        ordering = ('code', 'name', )


class CodeListTreeModel(MPTTModel, CodeListModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def get_descendants_pks(self, include_self=False):
        return [d.pk for d in self.get_descendants(include_self)]

    class Meta(CodeListModel.Meta):
        abstract = True

#### END ABSTRACT CLASSES


#### CODE LISTS CLASSES

class Recipient(CodeListTreeModel):
    code_list = 'recipient'
    code_list_facet = 'recipient'

    INCOME_GROUPS = Choices(
        ('10016', 'ldc', _('LDC')),
        ('10017', 'lic', _('Other LIC')),
        ('10018', 'lmic', _('LMIC')),
        ('10019', 'umic', _('UMIC')),
        ('10024', 'unallocated', _('Part I Unallocated by income')),
        ('10025', 'madct', _('MADCT')),
    )

    income_group = models.CharField(choices=INCOME_GROUPS, max_length=16, blank=True)

    # isocodes and statistical data from wb
    iso_code = models.CharField(max_length=3, blank=True, null=True)
    iso_alpha2 = models.CharField(max_length=2, blank=True, null=True)
    popolazione = models.BigIntegerField(null=True, blank=True)
    crescita_popolazione = models.FloatField(null=True, blank=True)
    pil = models.BigIntegerField(null=True, blank=True)
    pil_procapite = models.IntegerField(null=True, blank=True)

    # utl = models.ForeignKey('projects.Utl', blank=True, null=True)

    @classmethod
    def get_map_totals(cls, field='commitment', **filters):
        filters = dict([
            ('activity__%s' % key, value)
            for key, value in filters.items()
        ])

        totali_territori_rs = get_model('codelists', 'Recipient').objects.filter(
            iso_code__isnull=False,
            **filters).annotate(tot=Sum('activity__%s' % field))

        totali_territori = []

        for t in totali_territori_rs:
            ret = {
                'label': t.name,
                'iso_code': t.iso_code.upper(),
                'value': (t.tot or 0.0) * settings.OPENAID_MULTIPLIER,
                'code': t.code
            }
            totali_territori.append(ret)

        return totali_territori

    class Meta:
        ordering = ('name', 'code', )

    class MPTTMeta:
        order_insertion_by = ['name', ]


class Donor(CodeListModel):
    code_list = 'donor'

    GROUPS = Choices(
        ('dac', _('DAC members')),
        ('multilateral', _('Multilateral donors')),
        ('non_dac', _('Non-DAC donors')),
        ('private', _('Private donors')),
    )

    group = models.CharField(choices=GROUPS, blank=True, max_length=16)


class Agency(CodeListModel):
    code_list = 'agency'
    code_list_facet = 'agencies'

    acronym = models.CharField(max_length=50, blank=True)
    donor = models.ForeignKey(Donor)

#### HIERARCHICAL CODE LISTS

class Channel(CodeListTreeModel):
    """
    Channels of delivery.
    """
    code_list = 'channel'

    acronym = models.CharField(max_length=50, blank=True)


class FinanceType(CodeListTreeModel):
    """
    Used to distinguish financial instruments, e.g. grants or loans.
    """
    code_list = 'finance_type'
    code_list_csv_field = 'finance_t'


class AidType(CodeListTreeModel):
    """
    Used to distinguish aid modalities.
    """
    code_list = 'aid_type'
    code_list_csv_field = 'aid_t'


class Sector(CodeListTreeModel):
    """
    Purposes of aid..
    """
    code_list = 'sector'
    code_list_csv_field = 'purposecode'

#### END CODE LISTS CLASSES

CODE_LISTS = [Recipient, Donor, Agency, Channel, FinanceType, AidType, Sector]
CODE_LIST_NAMES = [c.code_list for c in CODE_LISTS]
CODE_LISTS_DICT = dict(zip(CODE_LIST_NAMES, CODE_LISTS))


def get_codelist(name):
    return CODE_LISTS_DICT[name]