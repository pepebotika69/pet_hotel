from django.db import models

from apps.core.models.mixins import TimestampMixin, SoftDeleteMixin


class CitizenUniversityManager(models.Manager):
    """Manager for Citizen model with soft delete support"""

    def not_deleted(self):
        return super().get_queryset().filter(is_deleted=False)

    def deleted(self):
        return super().get_queryset().filter(is_deleted=True)


class CitizenUniversity(TimestampMixin, SoftDeleteMixin, models.Model):
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

    objects = CitizenUniversityManager()

    class Meta:
        verbose_name = 'Citizen University Relation'
        verbose_name_plural = 'Citizen University Relations'
        indexes = [
            models.Index(fields=['citizen', 'university']),
        ]

    def __str__(self):
        return f"{self.citizen.full_name} - {self.university.name}"

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @staticmethod
    def soft_delete_bulk(ids: list[int]):
        CitizenUniversity.objects.filter(id__in=ids).update(is_deleted=True)

    def hard_delete(self):
        self.delete()

    @staticmethod
    def hard_delete_bulk(ids: list[int]):
        CitizenUniversity.objects.filter(id__in=ids).delete()
