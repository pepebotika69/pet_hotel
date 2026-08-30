from django.db import models

from apps.core.models.mixins import TimestampMixin


class Partner(TimestampMixin, models.Model):
    """
    Partner model representing companies that own pet hotels
    """
    # Partner details
    name = models.CharField(
        max_length=255,
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name="Rating",
        help_text="Rating from 1.0 to 5.0",
        null=True,
        blank=True
    )

    #created_at = models.DateTimeField(
    #    auto_now_add=True,
    #)
    #modified_at = models.DateTimeField(
    #    auto_now=True,
    #)

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        return self.name
