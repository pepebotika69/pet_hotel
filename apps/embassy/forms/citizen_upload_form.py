from django import forms
from django.utils.translation import gettext_lazy as _


class CitizenUploadForm(forms.Form):
    file = forms.FileField(
        label=_("Excel file (.xlsx)"),
        help_text=_("First row must be headers. Unique key: main_email."),
    )

    def clean_file(self):
        f = self.cleaned_data["file"]
        if not f.name.endswith(".xlsx"):
            raise forms.ValidationError(_("Only .xlsx files are supported."))
        return f
