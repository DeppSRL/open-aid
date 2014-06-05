"""
Questo modulo contiene il mapping tra i campi del csv
e i campi dei modelli django.
"""
from django.db.models import get_model

__author__ = 'joke2k'

class MappingException(BaseException):
    pass

# CSV orderder column names
ALL_FIELDS = (
    'Year', 'donorcode', 'donorname', 'agencycode', 'agencyname', 'crsid', 
    'projectnumber', 'initialreport', 'recipientcode', 'recipientname', 
    'regioncode', 'regionname', 'incomegroupcode', 'incomegroupname', 'flowcode', 
    'flowname', 'bi_multi', 'category', 'finance_t', 'aid_t', 'usd_commitment', 
    'usd_disbursement', 'usd_received', 'usd_commitment_defl', 
    'usd_disbursement_defl', 'usd_received_defl', 'usd_adjustment', 
    'usd_adjustment_defl', 'usd_amountuntied', 'usd_amountpartialtied', 
    'usd_amounttied', 'usd_amountuntied_defl', 'usd_amountpartialtied_defl', 
    'usd_amounttied_defl', 'usd_IRTC', 'usd_expert_commitment', 
    'usd_expert_extended', 'usd_export_credit', 'currencycode', 
    'commitment_national', 'disbursement_national', 'shortdescription', 
    'projecttitle', 'purposecode', 'purposename', 'sectorcode', 'sectorname', 
    'channelcode', 'channelname', 'channelreportedname', 'geography', 
    'expectedstartdate', 'completiondate', 'longdescription', 'gender', 
    'environment', 'trade', 'pdgg', 'FTC', 'PBA', 'investmentproject', 
    'assocfinance', 'biodiversity', 'climateMitigation', 'climateAdaptation', 
    'desertification', 'commitmentdate', 'typerepayment', 'numberrepayment', 
    'interest1', 'interest2', 'repaydate1', 'repaydate2', 'grantelement', 
    'usd_interest', 'usd_outstanding', 'usd_arrears_principal', 
    'usd_arrears_interest', 'usd_future_DS_principal', 'usd_future_DS_interest', 
)

EXCLUDED_FIELDS = (
    # see openaid.settings.OPENAID_DONOR
    'donorcode', 'donorname', 
    # mistery fields
    'category',
    'assocfinance',
    'typerepayment',
    'interest1',
    'interest2',
    'repaydate1',
    'repaydate2',
)

PARSABLE_FIELDS = [field for field in ALL_FIELDS if field not in EXCLUDED_FIELDS]

# Mapping CSV fields and Model fields

PROJECT_FIELDS_MAP = {
    'crsid': 'crs',
}

CHANNEL_REPORTED_MAP = {
    'channelreportedname': 'name',
}

MARKERS_FIELDS_MAP = {
    'biodiversity': 'biodiversity',
    'climateAdaptation': 'climate_adaptation',
    'climateMitigation': 'climate_mitigation',
    'desertification': 'desertification',
    'environment': 'environment',
    'gender': 'gender',
    'pdgg': 'pd_gg',
    'trade': 'trade',
}

ACTIVITY_FIELDS_MAP = {
    'Year': 'year',
    'projecttitle': 'title',
    'projectnumber': 'number',
    'shortdescription': 'description',
    'longdescription': 'long_description',
    'initialreport': 'report_type',
    'FTC': 'is_ftc',
    'PBA': 'is_pba',
    'investmentproject': 'is_investment',
    'geography': 'geography',
    'bi_multi': 'outflow',

    'grantelement': 'grant_element',
    'numberrepayment': 'number_repayment',
    'commitment_national': 'commitment_national',
    'disbursement_national': 'disbursement_national',
    'expectedstartdate': 'expected_start_date',
    'completiondate': 'completion_date',
    'commitmentdate': 'commitment_date',

    'currencycode': 'currency',
    'usd_commitment': 'usd_commitment',
    'usd_disbursement': 'usd_disbursement',

    'usd_received': 'usd_received',
    'usd_commitment_defl': 'usd_commitment_defl',
    'usd_disbursement_defl': 'usd_disbursement_defl',
    'usd_received_defl': 'usd_received_defl',
    'usd_adjustment': 'usd_adjustment',
    'usd_adjustment_defl': 'usd_adjustment_defl',
    'usd_amountuntied': 'usd_amount_untied',
    'usd_amountpartialtied': 'usd_amount_partialtied',
    'usd_amounttied': 'usd_amount_tied',
    'usd_amountuntied_defl': 'usd_amount_untied_defl',
    'usd_amountpartialtied_defl': 'usd_amount_partialtied_defl',
    'usd_amounttied_defl': 'usd_amount_tied_defl',
    'usd_IRTC': 'usd_IRTC',
    'usd_expert_commitment': 'usd_expert_commitment',
    'usd_expert_extended': 'usd_expert_extended',
    'usd_export_credit': 'usd_export_credit',
    'usd_interest': 'usd_interest',
    'usd_outstanding': 'usd_outstanding',
    'usd_arrears_principal': 'usd_arrears_principal',
    'usd_arrears_interest': 'usd_arrears_interest',
    'usd_future_DS_principal': 'usd_future_DS_principal',
    'usd_future_DS_interest': 'usd_future_DS_interest',
}



def convert_names(data, names_map):
    """
    Dato un dict questa funzione ritorna un dict con i nomi
    opportunamente convertiti dalla mappa di coversione fornita..
    """
    converted_row = {}
    for csv_key, model_field in names_map.items():
        converted_row[model_field] = data[csv_key]
    return converted_row


def create_mapped_form(form_class, data, names_map, **kwargs):
    """
    Data una classe Form, un dict di dati e un dict di mappatura dei nomi dei campi,
    questa funzione esegue la conversione dei campi e la passa al form
    per creare una nuova istanza.
    """
    form_data = convert_names(data, names_map)
    return form_class(data=form_data, **kwargs)
