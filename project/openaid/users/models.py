from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    city = models.CharField(max_length=200, blank=True)
    nation = models.OneToOneField('codelists.Recipient', null=True, blank=True, related_name='+')
    recipient_set = models.ManyToManyField('codelists.Recipient', blank=True)

    class Meta:
        db_table = 'auth_user'