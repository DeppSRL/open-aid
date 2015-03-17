from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _

class Attachment(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        return super(Attachment, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Photo(Attachment):
    file = models.ImageField(upload_to='photos/')


class Document(Attachment):

    file = models.FileField(upload_to='documents/', blank=True, null=True)
    source_url = models.URLField(help_text=_('Se non caricato direttamente indicare l\'indirizzo dove poter scaricare il documento.'), blank=True)