from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.embassy.models import University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    """Admin configuration for University model"""

    list_display = ["id", "created_at", "name", "city_code", "region_code"]
    list_filter = ["city_code", "region_code"]
    search_fields = ["name", "city_code", "region_code"]
    fieldsets = (
        (_("University Information"), {"fields": ("name", "main_address")}),
        (_("Location"), {"fields": ("city_code", "region_code")}),
    )
