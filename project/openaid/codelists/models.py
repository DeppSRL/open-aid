from django.db import models
from django.utils.translation import ugettext as _
from model_utils import Choices
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

#### ABSTRACT CLASSES

class CodeListModel(models.Model):

    code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=512, blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return u"<{0}:{1}> {2}".format(self.code_list, self.code, self.__unicode__())

    class Meta:
        abstract = True
        ordering = ('code', 'name', )


class CodeListTreeModel(MPTTModel, CodeListModel):

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class Meta(CodeListModel.Meta):
        abstract = True

#### END ABSTRACT CLASSES


#### CODE LISTS CLASSES

class Recipient(CodeListTreeModel):

    code_list = 'recipient'

    INCOME_GROUPS = Choices(
        (10016, 'ldc', _('LDC')),
        (10017, 'lic', _('Other LIC')),
        (10018, 'lmic', _('LMIC')),
        (10019, 'umic', _('UMIC')),
        (10024, 'unallocated', _('Part I Unallocated by income')),
        (10025, 'madct', _('MADCT')),
    )

    income_group = models.CharField(choices=INCOME_GROUPS, max_length=16, blank=True)


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
