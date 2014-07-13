from django.conf import settings


def currency_converter(amount, year):
    return amount * settings.OPENAID_CURRENCY_CONVERSIONS[year]
