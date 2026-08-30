from django.db import models

from apps.core.models.mixins import TimestampMixin
from apps.hotel.core.defs.city_codes import CityCodes
from apps.hotel.core.defs.region_codes import RegionCodes
from apps.hotel.models.partner import Partner


class Hotel(TimestampMixin, models.Model):
    """
    Pet Hotel model with location, rating, and partner relationship
    """
    # Foreign key to Partner
    partner = models.ForeignKey(
        Partner,
        on_delete=models.PROTECT,
        related_name='hotels',

    )

    # Hotel details
    address = models.TextField()
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name="Rating",
        help_text="Rating from 1.0 to 5.0",
        null=True,
        blank=True,
        db_index=True,
    )
    city_code = models.CharField(
        max_length=100,
        choices=CityCodes.get_choices(),
        db_index=True,
    )
    region_code = models.CharField(
        max_length=100,
        choices=RegionCodes.get_choices(),
        db_index=True,
    )

    #created_at = models.DateTimeField(
    #    auto_now_add=True,
    #)
    #modified_at = models.DateTimeField(
    #    auto_now=True,
    #)

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'
        indexes = [
            models.Index(fields=['city_code', 'region_code']),
        ]

    def __str__(self):
        return f"{self.partner.name} - Hotel (ID: {self.id})"
