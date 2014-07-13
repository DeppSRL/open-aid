from django.contrib.contenttypes.generic import GenericTabularInline
from .models import Photo


class PhotoInlineAdmin(GenericTabularInline):
    model = Photo
    extra = 1