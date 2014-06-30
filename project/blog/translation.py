from modeltranslation.translator import translator, TranslationOptions
from .models import Entry

class EntryTranslationOptions(TranslationOptions):
    fields = ('title', 'abstract', 'body')

translator.register(Entry, EntryTranslationOptions)
