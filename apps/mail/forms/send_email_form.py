from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from apps.embassy.models import Citizen
from apps.mail.models import MailTemplate
from apps.utils.enum import StrEnum


class RecipientSource(StrEnum):
    CITIZEN = "citizen"
    USER = "user"


RECIPIENT_SOURCE_MODELS = {
    RecipientSource.CITIZEN: Citizen,
    RecipientSource.USER: get_user_model(),
}


class UserWithEmailChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.username} ({obj.email})"


class SendEmailForm(forms.Form):
    mail_template = forms.ModelChoiceField(
        queryset=MailTemplate.objects.none(),
        label=_("Mail template"),
        empty_label=None,
    )
    recipient_source = forms.ChoiceField(
        choices=RecipientSource.get_choices(),
        widget=forms.RadioSelect,
        initial=RecipientSource.CITIZEN,
        label=_("Recipient source"),
    )
    citizen_recipients = forms.ModelMultipleChoiceField(
        queryset=Citizen.objects.not_deleted(),
        widget=FilteredSelectMultiple(_("citizens"), is_stacked=False),
        label=_("Citizens"),
        required=False,
    )
    user_recipients = UserWithEmailChoiceField(
        queryset=get_user_model().objects.filter(is_active=True).exclude(email=""),
        widget=FilteredSelectMultiple(_("users"), is_stacked=False),
        label=_("Users"),
        required=False,
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        source = (self.data or {}).get("recipient_source") or RecipientSource.CITIZEN
        model_class = RECIPIENT_SOURCE_MODELS.get(source)
        if model_class:
            ct = ContentType.objects.get_for_model(model_class)
            qs = MailTemplate.objects.filter(content_type=ct)
            if user is not None and not user.is_superuser:
                qs = qs.filter(groups__in=user.groups.all()).distinct()
            self.fields["mail_template"].queryset = qs

        if user is not None and not user.is_superuser:
            self.fields["user_recipients"].queryset = (
                self.fields["user_recipients"].queryset.filter(groups__in=user.groups.all()).distinct()
            )

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get("recipient_source")
        if source == RecipientSource.CITIZEN and not cleaned_data.get("citizen_recipients"):
            self.add_error("citizen_recipients", _("Please select at least one citizen."))
        elif source == RecipientSource.USER and not cleaned_data.get("user_recipients"):
            self.add_error("user_recipients", _("Please select at least one user."))
        return cleaned_data

    def get_recipient_emails(self) -> list[str]:
        source = self.cleaned_data["recipient_source"]
        if source == RecipientSource.CITIZEN:
            return [c.main_email for c in self.cleaned_data["citizen_recipients"]]
        if source == RecipientSource.USER:
            return [u.email for u in self.cleaned_data["user_recipients"]]
        return []
