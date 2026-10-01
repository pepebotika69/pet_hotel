from django import forms
from django.utils.translation import gettext_lazy as _

from apps.embassy.models import Citizen


class CitizenForm(forms.ModelForm):
    class Meta:
        model = Citizen
        fields = [
            "id_number",
            "first_name",
            "second_name",
            "first_surname",
            "second_surname",
            "birthdate",
            "main_email",
            "secondary_email",
            "phone_exterior",
            "phone_home_country",
        ]
        widgets = {
            "birthdate": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "id_number": _("ID Number"),
            "first_name": _("First Name"),
            "second_name": _("Second Name"),
            "first_surname": _("First Surname"),
            "second_surname": _("Second Surname"),
            "birthdate": _("Birthdate"),
            "main_email": _("Email"),
            "secondary_email": _("Secondary Email"),
            "phone_exterior": _("Phone (exterior)"),
            "phone_home_country": _("Phone (home country)"),
        }
