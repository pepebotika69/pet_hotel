from django.contrib import admin, messages
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from apps.mail.forms.send_email_form import RECIPIENT_SOURCE_MODELS, SendEmailForm
from apps.mail.models import MailTemplate, SentEmail, SentEmailStatus


@admin.register(MailTemplate)
class MailTemplateAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "content_type", "created_at", "modified_at"]
    search_fields = ["name"]
    fieldsets = ((_("Mail Template"), {"fields": ("content_type", "name", "html")}),)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        ct_ids = [ContentType.objects.get_for_model(m).id for m in RECIPIENT_SOURCE_MODELS.values()]
        form.base_fields["content_type"].queryset = ContentType.objects.filter(id__in=ct_ids)
        return form

    def get_urls(self):
        return [
            path(
                "send-email/",
                self.admin_site.admin_view(self.send_email_view),
                name="mail_mailtemplate_send_email",
            ),
        ] + super().get_urls()

    def send_email_view(self, request):
        if request.method == "POST":
            form = SendEmailForm(request.POST)
            if form.is_valid():
                template = form.cleaned_data["mail_template"]
                recipient_emails = form.get_recipient_emails()
                sent = 0
                failed = 0
                for recipient_email in recipient_emails:
                    try:
                        email = EmailMessage(
                            subject=template.name,
                            body=template.html,
                            to=[recipient_email],
                        )
                        email.content_subtype = "html"
                        email.send()
                        SentEmail.objects.create(
                            to=recipient_email,
                            status=SentEmailStatus.SENT,
                            template=template,
                        )
                        sent += 1
                    except Exception as e:
                        SentEmail.objects.create(
                            to=recipient_email,
                            status=SentEmailStatus.FAILED,
                            template=template,
                            error=str(e),
                        )
                        failed += 1

                if sent:
                    self.message_user(request, _("%d emails sent successfully.") % sent, messages.SUCCESS)
                if failed:
                    self.message_user(request, _("%d emails failed to send.") % failed, messages.ERROR)

                return redirect(reverse("admin:mail_mailtemplate_changelist"))
        else:
            form = SendEmailForm()

        source_to_ct_id = {
            source: ContentType.objects.get_for_model(model_class).id
            for source, model_class in RECIPIENT_SOURCE_MODELS.items()
        }
        templates_data = list(MailTemplate.objects.values("id", "name", "content_type_id"))

        context = {
            **self.admin_site.each_context(request),
            "title": _("Send Email"),
            "form": form,
            "opts": self.model._meta,
            "media": self.media + form.media,
            "source_to_ct_id": source_to_ct_id,
            "templates_data": templates_data,
        }
        return render(request, "admin/mail/send_email.html", context)
