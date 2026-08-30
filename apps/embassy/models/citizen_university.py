from django.db import models

from apps.core.models.mixins import TimestampMixin



class CitizenUniversity(TimestampMixin, models.Model):
    """
    """
    citizen = models.ForeignKey(
        'Citizen',
        on_delete=models.CASCADE,
        related_name='citizen_university_relations'
    )
    university = models.ForeignKey(
        'University',
        on_delete=models.CASCADE,
        related_name='university_citizen_relations'
    )

    # Additional fields specific to the relationship
    enrollment_date = models.DateField(
        help_text="Enrollment Date",
        null=True,
        blank=True
    )
    graduation_date = models.DateField(
        help_text="Graduation Date",
        null=True,
        blank=True
    )
    stop_date = models.DateField(
        help_text="Date when student stop attending to university. May be the same as graduation_date",
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is Active Student"
    )

    class Meta:
        verbose_name = 'Citizen University Relation'
        verbose_name_plural = 'Citizen University Relations'
        indexes = [
            models.Index(fields=['citizen', 'university']),
        ]

    def __str__(self):
        return f"{self.citizen.full_name} - {self.university.name}"
