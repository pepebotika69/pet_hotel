from datetime import date

from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.mixins import TimestampMixin, SoftDeleteMixin


class CitizenManager(models.Manager):
    """Manager for Citizen model with soft delete support"""

    def not_deleted(self):
        """Return only non-deleted citizens by default"""
        return super().get_queryset().filter(is_deleted=False)

    def deleted(self):
        """Return only soft-deleted citizens"""
        return super().get_queryset().filter(is_deleted=True)


class Citizen(TimestampMixin, SoftDeleteMixin, models.Model):
    """
    Citizen model with personal information and contact details
    """
    # FKs
    universities = models.ManyToManyField(
        'University',
        related_name='citizens',
        blank=True,
        null=True,
        through='CitizenUniversity',
        verbose_name=_('universities'),
    )
    # Personal Information
    first_name = models.CharField(
        max_length=100,
        verbose_name=_('first name'),
    )
    second_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('second name'),
    )
    first_surname = models.CharField(
        max_length=100,
        verbose_name=_('first surname'),
    )
    second_surname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('second surname'),
    )
    birthdate = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('birthdate'),
    )

    # Contact Information
    main_email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        verbose_name=_('main email'),
    )
    secondary_email = models.EmailField(
        validators=[EmailValidator()],
        blank=True,
        null=True,
        verbose_name=_('secondary email'),
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
        verbose_name=_('phone exterior'),
        help_text=_('Phone in exterior country'),
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
        verbose_name=_('phone home country'),
        help_text=_('Phone in home country'),
    )

    objects = CitizenManager()

    class Meta:
        verbose_name = _('Citizen')
        verbose_name_plural = _('Citizens')
        indexes = [
            models.Index(fields=['first_surname', 'first_name']),
            models.Index(fields=['main_email']),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.main_email})"

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @staticmethod
    def soft_delete_bulk(ids: list[int]):
        Citizen.objects.filter(id__in=ids).update(is_deleted=True)

    def hard_delete(self):
        self.delete()

    @staticmethod
    def hard_delete_bulk(ids: list[int]):
        Citizen.objects.filter(id__in=ids).delete()

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
