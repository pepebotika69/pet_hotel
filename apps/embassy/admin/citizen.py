from django.contrib import admin

from apps.embassy.models import CitizenUniversity, Citizen


class CitizenUniversityInline(admin.TabularInline):
    """Inline admin for CitizenUniversity relationships"""
    model = CitizenUniversity
    extra = 1
    fields = ['university', 'enrollment_date', 'graduation_date', 'stop_date', 'is_active']
    raw_id_fields = ['university']
    autocomplete_fields = ['university']


@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    """Admin configuration for Citizen model"""
    list_display = ['first_name', 'first_surname', 'main_email', 'age']
    list_filter = ['birthdate']
    search_fields = ['first_name', 'second_name', 'first_surname', 'second_surname', 'main_email']
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'second_name', 'first_surname', 'second_surname', 'birthdate')
        }),
        ('Contact Information', {
            'fields': ('main_email', 'secondary_email')
        }),
        ('Phone Numbers', {
            'fields': ('phone_exterior', 'phone_home_country')
        }),
    )
    inlines = [CitizenUniversityInline]
