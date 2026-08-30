from datetime import date

from django.core.validators import EmailValidator, RegexValidator
from django.db import models

from apps.core.models.mixins import TimestampMixin


class Citizen(TimestampMixin, models.Model):
    """
    Citizen model with personal information and contact details
    """
    # FKs
    universities = models.ManyToManyField(
        'University',
        related_name='citizens',
        blank=True,
        null=True,
        through='CitizenUniversity'
    )
    # Personal Information
    first_name = models.CharField(
        max_length=100,
    )
    second_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    first_surname = models.CharField(
        max_length=100,
    )
    second_surname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    birthdate = models.DateField(
        blank=True,
        null=True,
    )

    # Contact Information
    main_email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
    )
    secondary_email = models.EmailField(
        validators=[EmailValidator()],
        blank=True,
        null=True,
    )

    # Phone Numbers
    phone_exterior = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-()]+$',
                message="Phone number must contain only digits, spaces, hyphens, parentheses, and optional +"
            )
        ],
        blank=True,
        null=True,
        help_text="Phone in Exterior Country"
    )
    phone_home_country = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-()]+$',
                message="Phone number must contain only digits, spaces, hyphens, parentheses, and optional +"
            )
        ],
        blank=True,
        null=True,
        help_text="Phone in Home Country"
    )

    class Meta:
        verbose_name = 'Citizen'
        verbose_name_plural = 'Citizens'
        indexes = [
            models.Index(fields=['first_surname', 'first_name']),
            models.Index(fields=['main_email']),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.main_email})"

    @property
    def full_name(self):
        """Return the full name with all available parts"""
        parts = [self.first_name]
        if self.second_name:
            parts.append(self.second_name)
        parts.append(self.first_surname)
        if self.second_surname:
            parts.append(self.second_surname)
        return ' '.join(parts)

    @property
    def age(self):
        """Calculate age based on birthdate"""
        if self.birthdate:
            today = date.today()
            return today.year - self.birthdate.year - (
                    (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
            )
        return None
