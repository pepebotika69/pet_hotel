from django.db import models

from apps.core.models.mixins import TimestampMixin
from apps.hotel.core.defs.city_codes import CityCodes
from apps.hotel.core.defs.region_codes import RegionCodes


class University(TimestampMixin, models.Model):
    """
    University model with location information and one-to-one relation to Citizen
    """
    # University Information
    name = models.CharField(
        max_length=255,
    )
    main_address = models.TextField(
        null=True,
        blank=True
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

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'
        indexes = [
            models.Index(fields=['city_code', 'region_code']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.city_code})"
