from django.contrib import admin

from apps.embassy.models import CitizenUniversity
from apps.embassy.models import University


class UniversityCitizenInline(admin.TabularInline):
    """Inline admin for University relationships"""
    model = CitizenUniversity
    extra = 1
    fields = ['citizen', 'enrollment_date', 'graduation_date', 'stop_date', 'is_active']
    raw_id_fields = ['citizen']
    autocomplete_fields = ['citizen']


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    """Admin configuration for University model"""
    list_display = ['name', 'city_code', 'region_code']
    list_filter = ['city_code', 'region_code']
    search_fields = ['name', 'city_code', 'region_code']
    fieldsets = (
        ('University Information', {
            'fields': ('name', 'main_address')
        }),
        ('Location', {
            'fields': ('city_code', 'region_code')
        }),
        ('Contact Person', {
            'fields': ('citizen',)
        }),
    )
    inlines = [UniversityCitizenInline]
    raw_id_fields = ['citizen']
