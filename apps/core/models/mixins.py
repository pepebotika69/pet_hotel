from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        abstract = True
