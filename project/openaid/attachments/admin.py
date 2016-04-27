from modeltranslation.admin import TranslationGenericStackedInline
from .models import Photo, Document


class PhotoInlineAdmin(TranslationGenericStackedInline):
    model = Photo
    extra = 1


class DocumentInlineAdmin(TranslationGenericStackedInline):
    model = Document
    extra = 1