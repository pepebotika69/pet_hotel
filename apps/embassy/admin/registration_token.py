from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.embassy.models.registration_token import RegistrationToken


@admin.register(RegistrationToken)
class RegistrationTokenAdmin(admin.ModelAdmin):
    list_display = ["label", "created_at", "expires_at", "used_at", "status"]
    readonly_fields = ["token", "used_at", "created_at", "modified_at", "registration_link"]
    fields = ["label", "expires_at", "token", "registration_link", "used_at", "created_at", "modified_at"]

    def changeform_view(self, request, *args, **kwargs):
        self._current_request = request
        return super().changeform_view(request, *args, **kwargs)

    def registration_link(self, obj):
        if not obj.pk:
            return "Save first to generate the link."
        url = self._current_request.build_absolute_uri(reverse("citizen_register", args=[obj.token]))
        return format_html(
            '<div style="display:flex;gap:8px;align-items:center">'
            '<input id="reg-link-{pk}" type="text" value="{url}" readonly '
            'style="width:480px;padding:6px 8px;font-family:monospace;font-size:0.85rem;border:1px solid #ccc;border-radius:4px">'
            '<button type="button" id="reg-link-btn-{pk}" '
            "onclick=\"(function(){{var i=document.getElementById('reg-link-{pk}');"
            "var b=document.getElementById('reg-link-btn-{pk}');"
            "navigator.clipboard.writeText(i.value).then(function(){{b.textContent='Copied!';"
            "setTimeout(function(){{b.textContent='Copy';}},2000);}});}})()\" "
            'style="padding:6px 16px;cursor:pointer;white-space:nowrap">Copy</button>'
            "</div>",
            pk=obj.pk,
            url=url,
        )

    registration_link.short_description = "Registration Link"

    def status(self, obj):
        if obj.is_used:
            return "Used"
        if obj.is_expired:
            return "Expired"
        return "Active"

    status.short_description = "Status"
