from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.mixins import TimestampMixin


class MailTemplate(TimestampMixin, models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('name'),
    )
    html = models.TextField(
        verbose_name=_('html'),
    )

    class Meta:
        verbose_name = _('Mail Template')
        verbose_name_plural = _('Mail Templates')

    def __str__(self):
        return self.name
