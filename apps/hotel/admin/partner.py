from django.contrib import admin

from apps.hotel.models import Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rating", "created_at")
    search_fields = ("name",)
