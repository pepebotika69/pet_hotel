from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.mixins import TimestampMixin
from apps.mail.models.mail_template import MailTemplate
from apps.utils.enum import StrEnum


class SentEmailStatus(StrEnum):
    SENT = "sent"
    FAILED = "failed"


class SentEmail(TimestampMixin, models.Model):
    to = models.EmailField(verbose_name=_("to"))
    status = models.CharField(
        max_length=10,
        choices=SentEmailStatus.get_choices(),
        verbose_name=_("status"),
    )
    template = models.ForeignKey(
        MailTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_emails",
        verbose_name=_("template"),
    )
    error = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("error"),
    )

    class Meta:
        verbose_name = _("Sent Email")
        verbose_name_plural = _("Sent Emails")

    def __str__(self):
        return f"{self.to} — {self.status}"
