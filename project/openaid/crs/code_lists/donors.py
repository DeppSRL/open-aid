# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from model_utils import Choices


__author__ = 'joke2k'


DONOR_GROUPS = []
DONORS = []
AGENCIES = []


class CodeName(object):

    ALL = []

    def __init__(self, code, name, *args, **kwargs):
        self.code = code
        self.name = name
        self.__class__.ALL.append(self)

    @classmethod
    def get_all(cls, *code_set):
        if len(code_set) == 0:
            return cls.ALL
        return [obj for obj in cls.ALL if obj.code in code_set]

    @classmethod
    def get_by_code(cls, code):
        for group in cls.ALL:
            if group.code == code:
                return group
        raise Exception("Code '%s' not found" % code)

class DonorGroup(CodeName):

    ALL = DONOR_GROUPS

    def __init__(self, code, name, *args, **kwargs):
        super(DonorGroup, self).__init__(code, name, *args, **kwargs)
        self.donors = []

    def get_donor_list(self, *donor_code_set):
        return [donor for donor in Donor.get_all(*donor_code_set) if self in donor.groups]

    def get_donor_choices(self, *donor_code_set):
        return Choices(*[(d.code, d.name) for d in self.get_donor_list(*donor_code_set)])

    @classmethod
    def get_currency_choices(cls, *code_set):
        choices = Choices()
        for group in cls.get_all(*code_set):
            choices += group.get_donor_choices()
        return choices

class Donor(CodeName):

    ALL = DONORS

    def __init__(self, code, name, groups, *args, **kwargs):
        super(Donor, self).__init__(code, name, *args, **kwargs)
        groups = [groups] if isinstance(groups, basestring) else groups
        self.groups = []
        for group in groups:
            self.groups.append(DonorGroup.get_by_code(group))

class Agency(CodeName):

    ALL = AGENCIES

    def __init__(self, code, name, donor, *args, **kwargs):
        super(Agency, self).__init__(code, name, *args, **kwargs)
        self.donor = Donor.get_by_code(donor)


def generate_data():

    DonorGroup('dac', _('DAC members'))
    DonorGroup('multilateral', _('Multilateral donors'))
    DonorGroup('non_dac', _('Non-DAC donors'))
    DonorGroup('private', _('Private donors'))

    # add donors
    Donor(1, _('Austria'), 'dac'),
    Donor(2, _('Belgium'), 'dac'),
    Donor(3, _('Denmark'), 'dac'),
    Donor(4, _('France'), 'dac'),
    Donor(5, _('Germany'), 'dac'),
    Donor(6, _('Italy'), 'dac'),
    Donor(7, _('Netherlands'), 'dac'),
    Donor(8, _('Norway'), 'dac'),
    Donor(9, _('Portugal'), 'dac'),
    Donor(10, _('Sweden'), 'dac'),
    Donor(11, _('Switzerland'), 'dac'),
    Donor(12, _('United Kingdom'), 'dac'),
    Donor(18, _('Finland'), 'dac'),
    Donor(20, _('Iceland'), 'dac'),
    Donor(21, _('Ireland'), 'dac'),
    Donor(22, _('Luxembourg'), 'dac'),
    Donor(40, _('Greece'), 'dac'),
    Donor(50, _('Spain'), 'dac'),
    Donor(61, _('Slovenia'), 'dac'),
    Donor(68, _('Czech Republic'), 'dac'),
    Donor(69, _('Slovak Republic'), 'dac'),
    Donor(76, _('Poland'), 'dac'),
    Donor(301, _('Canada'), 'dac'),
    Donor(302, _('United States'), 'dac'),
    Donor(701, _('Japan'), 'dac'),
    Donor(742, _('Korea'), 'dac'),
    Donor(801, _('Australia'), 'dac'),
    Donor(820, _('New Zealand'), 'dac'),
    Donor(918, _('EU Institutions'), 'dac'),

    Donor(104, _('Nordic Dev.Fund'), 'multilateral'),
    Donor(807, _('UNEP'), 'multilateral'),
    Donor(811, _('GEF'), 'multilateral'),
    Donor(812, _('Montreal Protocol'), 'multilateral'),
    Donor(901, _('IBRD'), 'multilateral'),
    Donor(903, _('IFC'), 'multilateral'),
    Donor(905, _('IDA'), 'multilateral'),
    Donor(906, _('CarDB'), 'multilateral'),
    Donor(907, _('IMF'), 'multilateral'),
    Donor(909, _('IDB'), 'multilateral'),
    Donor(912, _('IDB Sp.Fund'), 'multilateral'),
    Donor(913, _('AfDB'), 'multilateral'),
    Donor(914, _('AfDF'), 'multilateral'),
    Donor(915, _('AsDB'), 'multilateral'),
    Donor(916, _('AsDB Special Funds'), 'multilateral'),
    Donor(921, _('Arab Fund (AFESD)'), 'multilateral'),
    Donor(923, _('UNPBF'), 'multilateral'),
    Donor(928, _('WHO'), 'multilateral'),
    Donor(944, _('IAEA'), 'multilateral'),
    Donor(948, _('UNECE'), 'multilateral'),
    Donor(951, _('OFID'), 'multilateral'),
    Donor(953, _('BADEA'), 'multilateral'),
    Donor(958, _('IMF (Concessional Trust Funds)'), 'multilateral'),
    Donor(959, _('UNDP'), 'multilateral'),
    Donor(960, _('UNTA'), 'multilateral'),
    Donor(963, _('UNICEF'), 'multilateral'),
    Donor(964, _('UNRWA'), 'multilateral'),
    Donor(966, _('WFP'), 'multilateral'),
    Donor(967, _('UNHCR'), 'multilateral'),
    Donor(971, _('UNAIDS'), 'multilateral'),
    Donor(974, _('UNFPA'), 'multilateral'),
    Donor(976, _('Isl.Dev Bank'), 'multilateral'),
    Donor(978, _('OSCE'), 'multilateral'),
    Donor(988, _('IFAD'), 'multilateral'),
    Donor(990, _('EBRD'), 'multilateral'),
    Donor(1311, _('GAVI'), 'multilateral'),
    Donor(1312, _('Global Fund'), 'multilateral'),

    Donor(30, _('Cyprus'), 'non_dac'),
    Donor(45, _('Malta'), 'non_dac'),
    Donor(55, _('Turkey'), 'non_dac'),
    Donor(70, _('Liechtenstein'), 'non_dac'),
    Donor(72, _('Bulgaria'), 'non_dac'),
    Donor(75, _('Hungary'), 'non_dac'),
    Donor(77, _('Romania'), 'non_dac'),
    Donor(82, _('Estonia'), 'non_dac'),
    Donor(83, _('Latvia'), 'non_dac'),
    Donor(84, _('Lithuania'), 'non_dac'),
    Donor(87, _('Russia'), 'non_dac'),
    Donor(130, _('Algeria'), 'non_dac'),
    Donor(133, _('Libya'), 'non_dac'),
    Donor(543, _('Iraq'), 'non_dac'),
    Donor(546, _('Israel'), 'non_dac'),
    Donor(552, _('Kuwait (KFAED)'), 'non_dac'),
    Donor(561, _('Qatar'), 'non_dac'),
    Donor(566, _('Saudi Arabia'), 'non_dac'),
    Donor(576, _('United Arab Emirates'), 'non_dac'),
    Donor(732, _('Chinese Taipei'), 'non_dac'),
    Donor(764, _('Thailand'), 'non_dac'),

    Donor(1601, _('Bill & Melinda Gates Foundation'), 'private'),

generate_data()