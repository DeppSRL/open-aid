from django.contrib import admin
from . import models

admin.site.register(models.Project)
admin.site.register(models.Activity)
admin.site.register(models.Markers)
admin.site.register(models.ChannelReported)
