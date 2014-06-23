from modeltranslation.translator import translator, TranslationOptions
from . import models

class CodeListTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

for code_list in models.CODE_LIST_MODELS:
    translator.register(code_list, CodeListTranslationOptions)

class ActivityTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'long_description', 'geography')

translator.register(models.Activity, ActivityTranslationOptions)