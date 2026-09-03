from django.contrib import admin, messages
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from apps.embassy.models import Citizen, CitizenUniversity


@admin.action(description=_("Restore selected citizens"))
def restore_citizens(modeladmin, request, queryset):
    """Restore soft-deleted citizens"""
    ids_to_restore = list(queryset.values_list("id", flat=True))

    count = len(ids_to_restore)
    if count > 0:
        with transaction.atomic():
            citizen_to_restore = Citizen.objects.filter(id__in=ids_to_restore)
            updated = citizen_to_restore.update(is_deleted=False)
            CitizenUniversity.objects.filter(citizen_id__in=ids_to_restore, is_deleted=True).update(is_deleted=False)

            modeladmin.message_user(request, _("%d citizens restored successfully.") % updated, messages.SUCCESS)
    else:
        modeladmin.message_user(request, _("No citizens selected for restore."), messages.WARNING)


@admin.action(description=_("Permanently delete selected citizens"))
def hard_delete_citizens(modeladmin, request, queryset):
    """Permanently delete selected citizens"""
    ids_to_delete = list(queryset.values_list("id", flat=True))

    count = len(ids_to_delete)
    if count > 0:
        with transaction.atomic():
            Citizen.hard_delete_bulk(ids=ids_to_delete)
            university_relations_to_delete = CitizenUniversity.objects.filter(
                citizen_id__in=ids_to_delete
            ).values_list("id", flat=True)
            CitizenUniversity.hard_delete_bulk(ids=university_relations_to_delete)

        modeladmin.message_user(request, _("%d citizens permanently deleted.") % count, messages.SUCCESS)
    else:
        modeladmin.message_user(request, _("No citizens selected for deletion."), messages.WARNING)


class CitizenUniversityInline(admin.TabularInline):
    """Inline admin for CitizenUniversity relationships"""

    model = CitizenUniversity
    extra = 1
    fields = ["university", "enrollment_date", "graduation_date", "stop_date", "is_active"]
    autocomplete_fields = ["university"]


@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    """Admin configuration for Citizen model"""

    list_display = ["id", "created_at", "first_name", "first_surname", "main_email", "age", "is_deleted"]
    list_filter = ["birthdate", "is_deleted"]
    search_fields = ["first_name", "second_name", "first_surname", "second_surname", "main_email"]
    fieldsets = (
        (
            _("Personal Information"),
            {"fields": ("first_name", "second_name", "first_surname", "second_surname", "birthdate")},
        ),
        (_("Contact Information"), {"fields": ("main_email", "secondary_email")}),
        (_("Phone Numbers"), {"fields": ("phone_exterior", "phone_home_country")}),
        (_("Status"), {"fields": ("is_deleted",)}),
    )
    inlines = [CitizenUniversityInline]
    actions = [restore_citizens, hard_delete_citizens]

    def get_queryset(self, request):
        """Override to show all citizens (including soft-deleted) by default"""
        qs = super().get_queryset(request)
        return qs

    def get_list_display(self, request):
        """Show deleted status in list"""
        return self.list_display

    def delete_model(self, request, obj):
        """Override delete method to use soft delete"""
        with transaction.atomic():
            obj.soft_delete()
            university_relations_to_delete = CitizenUniversity.objects.filter(citizen_id=obj.pk).values_list(
                "id", flat=True
            )
            CitizenUniversity.soft_delete_bulk(ids=university_relations_to_delete)

        self.message_user(request, _("%s was deleted successfully (soft delete).") % obj.full_name, messages.SUCCESS)

    def delete_queryset(self, request, queryset):
        """Override bulk delete to use soft delete"""
        with transaction.atomic():
            ids_to_delete = list(queryset.values_list("id", flat=True))
            Citizen.soft_delete_bulk(ids=ids_to_delete)
            university_relations_to_delete = CitizenUniversity.objects.filter(
                citizen_id__in=ids_to_delete
            ).values_list("id", flat=True)
            CitizenUniversity.soft_delete_bulk(ids=university_relations_to_delete)

        self.message_user(
            request, _("%d citizens were deleted successfully (soft delete).") % len(ids_to_delete), messages.SUCCESS
        )
