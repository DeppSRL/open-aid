from modeltranslation.translator import translator, TranslationOptions
from .models import Entry

__author__ = 'guglielmo'

class EntryTranslationOptions(TranslationOptions):
    fields = ('title', 'abstract', 'body')

translator.register(Entry, EntryTranslationOptions)
