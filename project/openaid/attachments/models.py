from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Attachment(models.Model):

    name = models.CharField(max_length=255)
    file = models.ImageField(upload_to='photo/')

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
    pass