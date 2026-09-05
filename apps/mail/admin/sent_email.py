from django.contrib import admin

from apps.mail.models import SentEmail


@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    list_display = ["id", "to", "template", "status", "error", "created_at", "modified_at"]
    list_filter = ["status", "template"]
    search_fields = ["to", "error"]
    readonly_fields = ["to", "template", "status", "error", "created_at", "modified_at"]
