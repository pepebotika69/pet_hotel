from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.embassy.models import MailTemplate


@admin.register(MailTemplate)
class MailTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'modified_at']
    search_fields = ['name']
    fieldsets = (
        (_('Mail Template'), {
            'fields': ('name', 'html')
        }),
    )
