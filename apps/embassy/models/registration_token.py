import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone

from apps.core.models.mixins import TimestampMixin


def _default_expires_at():
    return timezone.now() + timedelta(days=7)


class RegistrationToken(TimestampMixin, models.Model):
    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    label = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional note, e.g. intended recipient",
    )
    expires_at = models.DateTimeField(
        default=_default_expires_at,
    )
    used_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Registration Token"
        verbose_name_plural = "Registration Tokens"

    def __str__(self):
        return self.label or str(self.token)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def is_used(self):
        return self.used_at is not None

    @property
    def is_valid(self):
        return not self.is_expired and not self.is_used
