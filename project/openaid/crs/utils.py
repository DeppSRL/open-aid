from django.conf import settings
from . import models


usd_fields = [field for field in models.Activity._meta.get_all_field_names() if field.startswith('usd_')]


class CurrencyConverterError(BaseException):
    pass


def currency_converter(activity, save=False):
    """
    Questa funzione converte i valori dei campi usd_* nella currency di default del sito.
    Nel caso di errori lancia una CurrencyConverterError.
    Ritorna una lista di triple (usd_*field*, old_value, converted_value)

    :param activity:
    :param currency:
    :return:
    """
    converted_fields = []

    if activity.year not in settings.OPENAID_CURRENCY_CONVERSIONS:
        raise CurrencyConverterError('Activity year "%s" is not set into settings.OPENAID_CURRENCY_CONVERSIONS[%s]' % (activity.year, activity.currency))

    for usd_field in usd_fields:

        old_value = getattr(activity, usd_field)
        if old_value is None:
            continue
        new_value = old_value * settings.OPENAID_CURRENCY_CONVERSIONS[activity.year]
        setattr(activity, usd_field, new_value)
        converted_fields.append((usd_field, old_value, new_value))

    if save and len(converted_fields) > 0:
        activity.save()

    return converted_fields