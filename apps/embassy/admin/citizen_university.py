from django.contrib import admin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from apps.embassy.models import CitizenUniversity


@admin.action(description=_('Restore selected relations'))
def restore_citizens_universities(modeladmin, request, queryset):
    """Restore soft-deleted"""
    updated = queryset.update(is_deleted=False)
    modeladmin.message_user(
        request,
        f'{updated} relations restored successfully.',
        messages.SUCCESS
    )


@admin.action(description=_('Permanently delete selected relations'))
def hard_delete_citizens_universities(modeladmin, request, queryset):
    """Permanently delete selected"""
    ids_to_delete = list(queryset.values_list('id', flat=True))

    count = len(ids_to_delete)
    if count > 0:
        CitizenUniversity.hard_delete_bulk(ids=ids_to_delete)
        modeladmin.message_user(
            request,
            f'{count} relations permanently deleted.',
            messages.SUCCESS
        )
    else:
        modeladmin.message_user(
            request,
            'No relations selected for deletion.',
            messages.WARNING
        )


@admin.register(CitizenUniversity)
class CitizenUniversityAdmin(admin.ModelAdmin):
    """Admin configuration for CitizenUniversity relation"""
    list_display = ['id', 'created_at', 'citizen', 'university', 'is_active', 'is_deleted']
    list_filter = ['is_active', 'is_deleted']
    search_fields = ['citizen__first_name', 'citizen__first_surname', 'university__name']
    autocomplete_fields = ['citizen', 'university']
    fieldsets = (
        (_('Relations'), {
            'fields': ('citizen', 'university')
        }),
        (_('Status'), {
            'fields': ('enrollment_date', 'graduation_date', 'stop_date', 'is_active', 'is_deleted')
        }),
    )
    actions = [restore_citizens_universities, hard_delete_citizens_universities]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    def get_list_display(self, request):
        """Show deleted status in list"""
        return self.list_display

    def delete_model(self, request, obj):
        """Override delete method to use soft delete"""
        obj.soft_delete()

        self.message_user(
            request,
            f'{obj} was deleted successfully (soft delete).',
            messages.SUCCESS
        )

    def delete_queryset(self, request, queryset):
        """Override bulk delete to use soft delete"""
        ids_to_delete = list(queryset.values_list('id', flat=True))
        CitizenUniversity.soft_delete_bulk(ids=ids_to_delete)

        self.message_user(
            request,
            f'{len(ids_to_delete)} relations were deleted successfully (soft delete).',
            messages.SUCCESS
        )
