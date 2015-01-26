from modeltranslation.translator import translator, TranslationOptions
from . import models


class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description', )

translator.register(models.Project, ProjectTranslationOptions)


class ActivityTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'long_description', )

translator.register(models.Activity, ActivityTranslationOptions)