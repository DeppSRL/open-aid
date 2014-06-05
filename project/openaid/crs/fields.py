# coding=utf-8
from django.db import models
from model_utils import Choices
from django.utils.translation import ugettext as _

__author__ = 'joke2k'



class MarkerField(models.PositiveSmallIntegerField):
    """
    Questo campo rappresenta il contenuto di un Marker di un progetto.
    """

    choices = Choices(
        (None, 'blank', _('Not screened')),
        (0, 'not_targeted', _('Not targeted')),
        (1, 'significant_objective', _('Significant objective')),
        (2, 'principal_objective', _('Principal objective')),
    )

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'null': True,
            'blank': True,
        })
        super(MarkerField, self).__init__(*args, **kwargs)


class DesertificationMarkerField(MarkerField):
    """
    Questo marcatore prevede un opzione in più
    """

    choices = MarkerField.choices + Choices(
        (3, 'principal_objective', _('Principal objectives and in support of an action programme')),
    )
