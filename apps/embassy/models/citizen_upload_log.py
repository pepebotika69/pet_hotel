from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.mixins import TimestampMixin


class CitizenUploadLog(TimestampMixin, models.Model):
    log = models.JSONField(verbose_name=_("log"))

    class Meta:
        verbose_name = _("Citizen Upload Log")
        verbose_name_plural = _("Citizen Upload Logs")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Upload {self.pk} at {self.created_at}"
