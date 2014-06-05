from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from model_utils import Choices
from openaid.crs.code_lists.donors import CodeName

__author__ ='joke2k'


INCOME_GROUPS = []
REGIONS = []
RECIPIENTS = []

class IncomeGroup(CodeName):
    ALL = INCOME_GROUPS

class Region(CodeName):
    ALL = REGIONS

class Recipient(CodeName):

    ALL = RECIPIENTS

    def __init__(self, code, name, income_group, region, *args, **kwargs):
        super(Recipient, self).__init__(code, name, *args, **kwargs)
        self.region = Region.get_by_code(region) if region else None
        self.income_group = IncomeGroup.get_by_code(income_group) if income_group else None


def generate_data():
    """
    Income group:
    LDC (Least Developed Countries),
    Other LIC (Other Low Income Countries),
    LMICs (Lower Middle Income Countries and Territories),
    UMICs (Upper Middle Income Countries and Territories)
    """
    # from excel and dsd
    IncomeGroup(10016, _('LDC'))
    IncomeGroup(10017, _('Other LIC'))
    IncomeGroup(10018, _('LMIC'))
    IncomeGroup(10019, _('UMIC'))
    # from dsd and data
    IncomeGroup(10024, _('Part I Unallocated by income'))
    IncomeGroup(10025, _('MADCT'))

    # regions
    #Region(10100,'Developing Countries')
    Region(10010, _('Europe'))
    Region(10001, _('Africa'))
    Region(10002, _('North of Sahara'))
    Region(10003, _('South of Sahara'))
    Region(10004, _('America'))
    Region(10005, _('North & Central America'))
    Region(10006, _('South America'))
    Region(10007, _('Asia'))
    Region(10008, _('Far East Asia'))
    Region(10009, _('South & Central Asia'))
    Region(10011, _('Middle East'))
    Region(10012, _('Oceania'))
    #Region(9998, _('Developing Countries unspecified'))
    Region(15006, _('Developing Countries unspecified'))


    # recipients
    Recipient(30, _('Cyprus'), 10025, 10010)
    Recipient(35, _('Gibraltar'), 10025, 10010)
    Recipient(45, _('Malta'), 10025, 10010)
    Recipient(55, _('Turkey'), 10019, 10010)
    Recipient(57, _('Kosovo'), 10018, 10010)
    Recipient(61, _('Slovenia'), 10025, 10010)
    Recipient(62, _('Croatia'), 10025, 10010)
    Recipient(63, _('Serbia'), 10019, 10010)
    Recipient(64, _('Bosnia-Herzegovina'), 10019, 10010)
    Recipient(65, _('Montenegro'), 10019, 10010)
    Recipient(66, _('Macedonia, FYR'), 10019, 10010)
    Recipient(71, _('Albania'), 10019, 10010)
    Recipient(85, _('Ukraine'), 10018, 10010)
    Recipient(86, _('Belarus'), 10019, 10010)
    Recipient(88, _('States Ex-Yugoslavia unspecified'), None, 10010)
    Recipient(89, _('Europe, regional'), None, 10010)
    Recipient(93, _('Moldova'), 10018, 10010)
    Recipient(130, _('Algeria'), 10019, 10002)
    Recipient(133, _('Libya'), 10019, 10002)
    Recipient(136, _('Morocco'), 10018, 10002)
    Recipient(139, _('Tunisia'), 10019, 10002)
    Recipient(142, _('Egypt'), 10018, 10002)
    Recipient(189, _('North of Sahara, regional'), None, 10002)
    Recipient(218, _('South Africa'), 10019, 10003)
    Recipient(225, _('Angola'), 10016, 10003)
    Recipient(227, _('Botswana'), 10019, 10003)
    Recipient(228, _('Burundi'), 10016, 10003)
    Recipient(229, _('Cameroon'), 10018, 10003)
    Recipient(230, _('Cape Verde'), 10018, 10003)
    Recipient(231, _('Central African Rep.'), 10016, 10003)
    Recipient(232, _('Chad'), 10016, 10003)
    Recipient(233, _('Comoros'), 10016, 10003)
    Recipient(234, _('Congo, Rep.'), 10018, 10003)
    Recipient(235, _('Congo, Dem. Rep.'), 10016, 10003)
    Recipient(236, _('Benin'), 10016, 10003)
    Recipient(238, _('Ethiopia'), 10016, 10003)
    Recipient(239, _('Gabon'), 10019, 10003)
    Recipient(240, _('Gambia'), 10016, 10003)
    Recipient(241, _('Ghana'), 10018, 10003)
    Recipient(243, _('Guinea'), 10016, 10003)
    Recipient(244, _('Guinea-Bissau'), 10016, 10003)
    Recipient(245, _('Equatorial Guinea'), 10016, 10003)
    Recipient(247, _('Cote d\'Ivoire'), 10018, 10003)
    Recipient(248, _('Kenya'), 10017, 10003)
    Recipient(249, _('Lesotho'), 10016, 10003)
    Recipient(251, _('Liberia'), 10016, 10003)
    Recipient(252, _('Madagascar'), 10016, 10003)
    Recipient(253, _('Malawi'), 10016, 10003)
    Recipient(255, _('Mali'), 10016, 10003)
    Recipient(256, _('Mauritania'), 10016, 10003)
    Recipient(257, _('Mauritius'), 10019, 10003)
    Recipient(258, _('Mayotte'), 10025, 10003)
    Recipient(259, _('Mozambique'), 10016, 10003)
    Recipient(260, _('Niger'), 10016, 10003)
    Recipient(261, _('Nigeria'), 10018, 10003)
    Recipient(265, _('Zimbabwe'), 10017, 10003)
    Recipient(266, _('Rwanda'), 10016, 10003)
    Recipient(268, _('Sao Tome & Principe'), 10016, 10003)
    Recipient(269, _('Senegal'), 10016, 10003)
    Recipient(270, _('Seychelles'), 10019, 10003)
    Recipient(271, _('Eritrea'), 10016, 10003)
    Recipient(272, _('Sierra Leone'), 10016, 10003)
    Recipient(273, _('Somalia'), 10016, 10003)
    Recipient(274, _('Djibouti'), 10016, 10003)
    Recipient(275, _('Namibia'), 10019, 10003)
    Recipient(276, _('St. Helena'), 10019, 10003)
    Recipient(278, _('Sudan'), 10016, 10003)
    Recipient(279, _('South Sudan'), 10016, 10003)
    Recipient(280, _('Swaziland'), 10018, 10003)
    Recipient(282, _('Tanzania'), 10016, 10003)
    Recipient(283, _('Togo'), 10016, 10003)
    Recipient(285, _('Uganda'), 10016, 10003)
    Recipient(287, _('Burkina Faso'), 10016, 10003)
    Recipient(288, _('Zambia'), 10016, 10003)
    Recipient(289, _('South of Sahara, regional'), None, 10003)
    Recipient(298, _('Africa, regional'), None, 10001)
    Recipient(328, _('Bahamas'), 10025, 10005)
    Recipient(329, _('Barbados'), 10025, 10005)
    Recipient(331, _('Bermuda'), 10025, 10005)
    Recipient(336, _('Costa Rica'), 10019, 10005)
    Recipient(338, _('Cuba'), 10019, 10005)
    Recipient(340, _('Dominican Republic'), 10019, 10005)
    Recipient(342, _('El Salvador'), 10018, 10005)
    Recipient(347, _('Guatemala'), 10018, 10005)
    Recipient(349, _('Haiti'), 10016, 10005)
    Recipient(351, _('Honduras'), 10018, 10005)
    Recipient(352, _('Belize'), 10018, 10005)
    Recipient(354, _('Jamaica'), 10019, 10005)
    Recipient(358, _('Mexico'), 10019, 10005)
    Recipient(361, _('Netherlands Antilles'), 10025, 10005)
    Recipient(364, _('Nicaragua'), 10018, 10005)
    Recipient(366, _('Panama'), 10019, 10005)
    Recipient(373, _('Aruba'), 10025, 10005)
    Recipient(375, _('Trinidad and Tobago'), 10025, 10005)
    Recipient(376, _('Anguilla'), 10019, 10005)
    Recipient(377, _('Antigua and Barbuda'), 10019, 10005)
    Recipient(378, _('Dominica'), 10019, 10005)
    Recipient(380, _('West Indies, regional'), None, 10005)
    Recipient(381, _('Grenada'), 10019, 10005)
    Recipient(382, _('St. Kitts-Nevis'), 10019, 10005)
    Recipient(383, _('St. Lucia'), 10019, 10005)
    Recipient(384, _('St.Vincent & Grenadines'), 10019, 10005)
    Recipient(385, _('Montserrat'), 10019, 10005)
    Recipient(386, _('Cayman Islands'), 10025, 10005)
    Recipient(387, _('Turks and Caicos Islands'), 10025, 10005)
    Recipient(388, _('Virgin Islands (UK)'), 10025, 10005)
    Recipient(389, _('North & Central America, regional'), None, 10005)
    Recipient(425, _('Argentina'), 10019, 10006)
    Recipient(428, _('Bolivia'), 10018, 10006)
    Recipient(431, _('Brazil'), 10019, 10006)
    Recipient(434, _('Chile'), 10019, 10006)
    Recipient(437, _('Colombia'), 10019, 10006)
    Recipient(440, _('Ecuador'), 10019, 10006)
    Recipient(443, _('Falkland Islands (Malvinas)'), 10025, 10006)
    Recipient(446, _('Guyana'), 10018, 10006)
    Recipient(451, _('Paraguay'), 10018, 10006)
    Recipient(454, _('Peru'), 10019, 10006)
    Recipient(457, _('Suriname'), 10019, 10006)
    Recipient(460, _('Uruguay'), 10019, 10006)
    Recipient(463, _('Venezuela'), 10019, 10006)
    Recipient(489, _('South America, regional'), None, 10006)
    Recipient(498, _('America, regional'), None, 10004)
    Recipient(530, _('Bahrain'), 10025, 10011)
    Recipient(540, _('Iran'), 10019, 10011)
    Recipient(543, _('Iraq'), 10018, 10011)
    Recipient(546, _('Israel'), 10025, 10011)
    Recipient(549, _('Jordan'), 10019, 10011)
    Recipient(550, _('West Bank & Gaza Strip'), 10018, 10011)
    Recipient(552, _('Kuwait'), 10025, 10011)
    Recipient(555, _('Lebanon'), 10019, 10011)
    Recipient(558, _('Oman'), 10025, 10011)
    Recipient(561, _('Qatar'), 10025, 10011)
    Recipient(566, _('Saudi Arabia'), 10025, 10011)
    Recipient(573, _('Syria'), 10018, 10011)
    Recipient(576, _('United Arab Emirates'), 10025, 10011)
    Recipient(580, _('Yemen'), 10016, 10011)
    Recipient(589, _('Middle East, regional'), None, 10011)
    Recipient(610, _('Armenia'), 10018, 10009)
    Recipient(611, _('Azerbaijan'), 10019, 10009)
    Recipient(612, _('Georgia'), 10018, 10009)
    Recipient(613, _('Kazakhstan'), 10019, 10009)
    Recipient(614, _('Kyrgyz Republic'), 10017, 10009)
    Recipient(615, _('Tajikistan'), 10017, 10009)
    Recipient(616, _('Turkmenistan'), 10018, 10009)
    Recipient(617, _('Uzbekistan'), 10018, 10009)
    Recipient(619, _('Central Asia, regional'), None, 10009)
    Recipient(625, _('Afghanistan'), 10016, 10009)
    Recipient(630, _('Bhutan'), 10016, 10009)
    Recipient(635, _('Myanmar'), 10016, 10009)
    Recipient(640, _('Sri Lanka'), 10018, 10009)
    Recipient(645, _('India'), 10018, 10009)
    Recipient(655, _('Maldives'), 10019, 10009)
    Recipient(660, _('Nepal'), 10016, 10009)
    Recipient(665, _('Pakistan'), 10018, 10009)
    Recipient(666, _('Bangladesh'), 10016, 10009)
    Recipient(679, _('South Asia, regional'), None, 10009)
    Recipient(689, _('South & Central Asia, regional'), None, 10009)
    Recipient(725, _('Brunei'), 10025, 10008)
    Recipient(728, _('Cambodia'), 10016, 10008)
    Recipient(730, _('China'), 10019, 10008)
    Recipient(732, _('Chinese Taipei'), 10025, 10008)
    Recipient(735, _('Hong Kong, China'), 10025, 10008)
    Recipient(738, _('Indonesia'), 10018, 10008)
    Recipient(740, _('Korea, Dem. Rep.'), 10017, 10008)
    Recipient(742, _('Korea'), 10025, 10008)
    Recipient(745, _('Laos'), 10016, 10008)
    Recipient(748, _('Macao'), 10025, 10008)
    Recipient(751, _('Malaysia'), 10019, 10008)
    Recipient(753, _('Mongolia'), 10018, 10008)
    Recipient(755, _('Philippines'), 10018, 10008)
    Recipient(761, _('Singapore'), 10025, 10008)
    Recipient(764, _('Thailand'), 10019, 10008)
    Recipient(765, _('Timor-Leste'), 10016, 10008)
    Recipient(769, _('Vietnam'), 10018, 10008)
    Recipient(789, _('Far East Asia, regional'), None, 10008)
    Recipient(798, _('Asia, regional'), None, 10007)
    Recipient(831, _('Cook Islands'), 10019, 10012)
    Recipient(832, _('Fiji'), 10018, 10012)
    Recipient(836, _('Kiribati'), 10016, 10012)
    Recipient(840, _('French Polynesia'), 10025, 10012)
    Recipient(845, _('Nauru'), 10019, 10012)
    Recipient(850, _('New Caledonia'), 10025, 10012)
    Recipient(854, _('Vanuatu'), 10016, 10012)
    Recipient(858, _('Northern Marianas'), 10025, 10012)
    Recipient(856, _('Niue'), 10019, 10012)
    Recipient(859, _('Marshall Islands'), 10018, 10012)
    Recipient(860, _('Micronesia, Fed. States'), 10018, 10012)
    Recipient(861, _('Palau'), 10019, 10012)
    Recipient(862, _('Papua New Guinea'), 10018, 10012)
    Recipient(866, _('Solomon Islands'), 10016, 10012)
    Recipient(868, _('Tokelau'), 10018, 10012)
    Recipient(870, _('Tonga'), 10018, 10012)
    Recipient(872, _('Tuvalu'), 10016, 10012)
    Recipient(876, _('Wallis & Futuna'), 10019, 10012)
    Recipient(880, _('Samoa'), 10016, 10012)
    Recipient(889, _('Oceania, regional'), None, 10012)
    Recipient(998, _('Developing countries, unspecified'), None, None)


generate_data()