from datetime import datetime
from django.db import models
from tagging import models as tagging_models
from django.utils.translation import ugettext_lazy as _

class Entry(tagging_models.TagMixin, models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True)
    abstract = models.TextField()
    body = models.TextField()
    published_at = models.DateTimeField(default=datetime.now(), verbose_name=_('Publishing date'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def save(self,
             force_insert=False, force_update=False,
             using=None,
             update_fields=None
    ):
        if not self.published_at:
            self.published_at = datetime.now()
        return super(Entry, self).save(force_insert, force_update, using)

    class Meta:
        ordering= ['-published_at']
        verbose_name= _('Entry')
        verbose_name_plural= _('Entries')

class Blog(object):

    @staticmethod
    def get_latest_entries(qnt=10, end_date=None, start_date=None, single=False):
        end_date = end_date or datetime.now()
        qnt = qnt if not single else 1

        if start_date:
            entries = Entry.objects.filter(published_at__range=(start_date, end_date))[:qnt]
        else :
            entries = Entry.objects.filter(published_at__lte=end_date)[:qnt]

        if single :
            return entries[0] if entries else None

        return entries
