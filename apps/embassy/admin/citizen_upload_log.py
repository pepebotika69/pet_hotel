from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.embassy.models.citizen_upload_log import CitizenUploadLog


@admin.register(CitizenUploadLog)
class CitizenUploadLogAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "summary_created", "summary_updated", "summary_errors", "total_rows"]
    readonly_fields = ["created_at", "modified_at", "log_display"]
    fields = ["created_at", "modified_at", "log_display"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def _counts(self, obj):
        created = updated = errors = 0
        for entry in obj.log or []:
            s = entry.get("status")
            if s == "created":
                created += 1
            elif s == "updated":
                updated += 1
            elif s == "error":
                errors += 1
        return created, updated, errors

    @admin.display(description=_("Created"))
    def summary_created(self, obj):
        return self._counts(obj)[0]

    @admin.display(description=_("Updated"))
    def summary_updated(self, obj):
        return self._counts(obj)[1]

    @admin.display(description=_("Errors"))
    def summary_errors(self, obj):
        return self._counts(obj)[2]

    @admin.display(description=_("Total rows"))
    def total_rows(self, obj):
        return len(obj.log or [])

    @admin.display(description=_("Log"))
    def log_display(self, obj):
        rows = obj.log or []
        if not rows:
            return "—"
        header = (
            "<table style='border-collapse:collapse;width:100%'>"
            "<thead><tr>"
            "<th style='border:1px solid #ccc;padding:4px 8px'>Row</th>"
            "<th style='border:1px solid #ccc;padding:4px 8px'>Status</th>"
            "<th style='border:1px solid #ccc;padding:4px 8px'>Email</th>"
            "<th style='border:1px solid #ccc;padding:4px 8px'>Message</th>"
            "</tr></thead><tbody>"
        )
        status_colors = {"created": "#2e7d32", "updated": "#1565c0", "error": "#c62828"}
        body = ""
        for entry in rows:
            status = entry.get("status", "")
            color = status_colors.get(status, "#000")
            body += (
                f"<tr>"
                f"<td style='border:1px solid #eee;padding:4px 8px'>{entry.get('row', '')}</td>"
                f"<td style='border:1px solid #eee;padding:4px 8px;color:{color};font-weight:bold'>{status}</td>"
                f"<td style='border:1px solid #eee;padding:4px 8px'>{entry.get('email', '')}</td>"
                f"<td style='border:1px solid #eee;padding:4px 8px;white-space:pre-wrap;font-size:11px'>"
                f"{entry.get('message', '')}</td>"
                f"</tr>"
            )
        return format_html(header + body + "</tbody></table>")
