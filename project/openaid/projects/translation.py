from modeltranslation.translator import translator, TranslationOptions
from . import models


class ActivityTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'long_description', )

translator.register(models.Activity, ActivityTranslationOptions)