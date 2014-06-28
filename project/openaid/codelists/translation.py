from modeltranslation.translator import translator, TranslationOptions
from . import models

class CodeListTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

for code_list in models.CODE_LISTS:
    translator.register(code_list, CodeListTranslationOptions)
