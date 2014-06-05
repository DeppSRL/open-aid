from model_utils import Choices

__author__ = 'joke2k'

from openaid.crs.code_lists.donors import CodeName

FINANCE_GROUPS = []
FINANCE_TYPES = []

class FinanceGroup(CodeName):

    ALL = FINANCE_GROUPS

    def __init__(self, code, name, description='', *args, **kwargs):
        super(FinanceGroup, self).__init__(code, name, *args, **kwargs)
        self.description = description

class FinanceType(CodeName):

    ALL = FINANCE_TYPES

    def __init__(self, code, name, *args, **kwargs):
        super(FinanceType, self).__init__(code, name, *args, **kwargs)
        self.group = FinanceGroup.get_by_code(code / 100 * 100)

    @classmethod
    def get_choices(cls):
        return Choices(*[(ft.code, ft.name) for ft in cls.get_all()])


def generate_data():
    FinanceGroup(0, 'NON FLOW ITEMS', 'Non resource flow items requested on DAC table 1')
    FinanceType(1, 'GNI: Gross National Income')
    FinanceType(2, 'ODA % GNI')
    FinanceType(3, 'Total flows % GNI')
    FinanceType(4, 'Population')

    FinanceGroup(100, 'GRANT', 'Transfers in cash or in kind for which no legal debt is incurred by the recipient.')
    FinanceType(110, 'Aid grant excluding debt reorganisation')
    FinanceType(111, 'Subsidies to national private investors')

    FinanceGroup(200, 'INTEREST SUBSIDY', 'Subsidies to soften the terms of private export credits, or loans or credits by the banking sector.')
    FinanceType(210, 'Interest subsidy grant in AF')
    FinanceType(211, 'Interest subsidy to national private exporters')

    FinanceGroup(300, 'CAPITAL SUBSCRIPTION', 'Payments to multilateral agencies in the form of notes and similar instruments, unconditionally cashable at sight by the recipient institutions.')
    FinanceType(310, 'Deposit basis')
    FinanceType(311, 'Encashment basis')

    FinanceGroup(400, 'LOAN', 'Transfers in cash or in kind for which the recipient incurs legal debt.')
    FinanceType(410, 'Aid loan excluding debt reorganisation')
    FinanceType(411, 'Investment-related loan to developing countries')
    FinanceType(412, 'Loan in a joint venture with the recipient')
    FinanceType(413, 'Loan to national private investor')
    FinanceType(414, 'Loan to national private exporter')

    FinanceGroup(450, 'EXPORT CREDIT', 'Official or private loans which are primarily export-facilitating in purpose.  They are usually tied to a specific export from the extending country and not represented by a negotiable instrument.')
    FinanceType(451, 'Non-banks guaranteed export credits')
    FinanceType(452, 'Non-banks non-guaranteed portions of guaranteed export credits')
    FinanceType(453, 'Bank export credits')

    FinanceGroup(500, 'EQUITY', 'Investment in a country on the DAC List of ODA Recipients that is not made to acquire a lasting interest in an enterprise.')
    FinanceType(510, 'Acquisition of equity as part of a joint venture with the recipient')
    FinanceType(511, 'Acquisition of equity not part of joint venture in developing countries')
    FinanceType(512, 'Other acquisition of equity')

    FinanceGroup(600, 'DEBT RELIEF', 'Debt cancellations, debt conversions, debt rescheduling within or outside the framework of the Paris Club.')
    FinanceType(610, 'Debt forgiveness:  ODA claims (P)')
    FinanceType(611, 'Debt forgiveness: ODA claims (I)')
    FinanceType(612, 'Debt forgiveness: OOF claims (P)')
    FinanceType(613, 'Debt forgiveness: OOF claims (I)')
    FinanceType(614, 'Debt forgiveness:  Private claims (P)')
    FinanceType(615, 'Debt forgiveness:  Private claims (I)')
    FinanceType(616, 'Debt forgiveness: OOF claims (DSR)')
    FinanceType(617, 'Debt forgiveness:  Private claims (DSR)')
    FinanceType(618, 'Debt forgiveness: Other')
    FinanceType(620, 'Debt rescheduling: ODA claims (P)')
    FinanceType(621, 'Debt rescheduling: ODA claims (I)')
    FinanceType(622, 'Debt rescheduling: OOF claims (P)')
    FinanceType(623, 'Debt rescheduling: OOF claims (I)')
    FinanceType(624, 'Debt rescheduling:  Private claims (P)')
    FinanceType(625, 'Debt rescheduling:  Private claims (I)')
    FinanceType(626, 'Debt rescheduling: OOF claims (DSR)')
    FinanceType(627, 'Debt rescheduling:  Private claims (DSR)')
    FinanceType(630, 'Debt rescheduling: OOF claim (DSR - original loan principal)')
    FinanceType(631, 'Debt rescheduling: OOF claim (DSR - original loan interest)')
    FinanceType(632, 'Debt rescheduling: Private claim (DSR - original loan principal)')

    FinanceGroup(700, 'INVESTMENT', 'Investment made by a private entity resident in a reporting country to acquire or add to a lasting interest(1) in an enterprise in a country on the DAC List of ODA Recipients.')
    FinanceType(710, 'Foreign direct investment')
    FinanceType(711, 'Other foreign direct investment, including reinvested earnings')

    FinanceGroup(800, 'BONDS', 'Acquisition of bonds issued by developing countries.')
    FinanceType(810, 'Bank bonds')
    FinanceType(811, 'Non-bank  bonds')

    FinanceGroup(900, 'OTHER SECURITIES/CLAIMS')
    FinanceType(910, 'Other bank securities/claims')
    FinanceType(911, 'Other non-bank securities/claims')
    FinanceType(912, 'Securities and other instruments issued by multilateral agencies')

generate_data()
