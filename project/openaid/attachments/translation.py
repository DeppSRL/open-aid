from modeltranslation.translator import translator, TranslationOptions
from . import models


class PhotoTranslationOptions(TranslationOptions):
    fields = ('name', 'description', )

translator.register(models.Photo, PhotoTranslationOptions)


class DocumentTranslationOptions(TranslationOptions):
    fields = ('name', 'description', )

translator.register(models.Document, DocumentTranslationOptions)
