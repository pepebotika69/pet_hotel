from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _

from apps.embassy.models import Citizen, MailTemplate


class SendEmailForm(forms.Form):
    mail_template = forms.ModelChoiceField(
        queryset=MailTemplate.objects.all(),
        label=_("Mail template"),
        empty_label=None,
    )
    citizens = forms.ModelMultipleChoiceField(
        queryset=Citizen.objects.not_deleted(),
        widget=FilteredSelectMultiple(
            _("citizens"),
            is_stacked=False,
        ),
        label=_("Citizens"),
    )
