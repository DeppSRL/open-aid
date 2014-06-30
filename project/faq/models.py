import datetime
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.db import models
from faq.managers import QuestionManager

__author__ = 'guglielmo'


class Question(models.Model):
    HEADER = 2
    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = (
        (ACTIVE,    _('Active')),
        (INACTIVE,  _('Inactive')),
    )

    text = models.TextField(_('question'), help_text=_('The actual question itself.'))
    answer = models.TextField(_('answer'), blank=True, help_text=_('The answer text.'))
    slug = models.SlugField(_('slug'), max_length=128)
    status = models.IntegerField(_('status'),
        choices=STATUS_CHOICES, default=INACTIVE,
        help_text=_("Only questions with their status set to 'Active' will be "
                    "displayed."))

    sort_order = models.IntegerField(_('sort order'), default=0,
        help_text=_('The order you would like the question to be displayed.'))

    created_on = models.DateTimeField(_('created on'), default=datetime.datetime.now)

    objects = QuestionManager()

    class Meta:
        verbose_name = _("Frequently asked question")
        verbose_name_plural = _("Frequently asked questions")
        ordering = ['sort_order', 'created_on']

    def __unicode__(self):
        return self.text

    def save(self, *args, **kwargs):
        # Set the date updated.
        self.updated_on = datetime.datetime.now()

        # Create a unique slug, if needed.
        if not self.slug:
            suffix = 0
            potential = base = slugify(self.text[:90])
            while not self.slug:
                if suffix:
                    potential = "%s-%s" % (base, suffix)
                if not Question.objects.filter(slug=potential).exists():
                    self.slug = potential
                # We hit a conflicting slug; increment the suffix and try again.
                suffix += 1

        super(Question, self).save(*args, **kwargs)

    def is_active(self):
        return self.status == Question.ACTIVE

