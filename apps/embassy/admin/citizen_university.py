from django.contrib import admin

from apps.embassy.models import CitizenUniversity


@admin.register(CitizenUniversity)
class CitizenUniversityAdmin(admin.ModelAdmin):
    """Admin configuration for CitizenUniversity relation"""
    list_display = ['citizen', 'university', 'is_active']
    list_filter = ['is_active']
    search_fields = ['citizen__first_name', 'citizen__first_surname', 'university__name']
    raw_id_fields = ['citizen', 'university']
    autocomplete_fields = ['citizen', 'university']
    fieldsets = (
        ('Relations', {
            'fields': ('citizen', 'university')
        }),
        ('Status', {
            'fields': ('enrollment_date', 'graduation_date', 'stop_date', 'is_active')
        }),
    )
