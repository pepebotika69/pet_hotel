from django.contrib import admin, messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from apps.embassy.forms.send_email_form import SendEmailForm
from apps.mail.models import MailTemplate, SentEmail, SentEmailStatus


@admin.register(MailTemplate)
class MailTemplateAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at", "modified_at"]
    search_fields = ["name"]
    fieldsets = ((_("Mail Template"), {"fields": ("name", "html")}),)

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
                citizens = form.cleaned_data["citizens"]
                sent = 0
                failed = 0
                for citizen in citizens:
                    try:
                        email = EmailMessage(
                            subject=template.name,
                            body=template.html,
                            to=[citizen.main_email],
                        )
                        email.content_subtype = "html"
                        email.send()
                        SentEmail.objects.create(
                            to=citizen.main_email,
                            status=SentEmailStatus.SENT,
                            template=template,
                        )
                        sent += 1
                    except Exception as e:
                        SentEmail.objects.create(
                            to=citizen.main_email,
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

        context = {
            **self.admin_site.each_context(request),
            "title": _("Send Email"),
            "form": form,
            "opts": self.model._meta,
            "media": self.media + form.media,
        }
        return render(request, "admin/mail/send_email.html", context)
