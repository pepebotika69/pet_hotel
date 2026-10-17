import logging

from django.core.mail import EmailMessage

from apps.embassy.defs.citizen_register import WELCOME_SP_TEMPLATE_NAME
from apps.embassy.models.citizen import Citizen
from apps.mail.models import MailTemplate, SentEmail, SentEmailStatus

logger = logging.getLogger(__name__)


def send_welcome_email(citizen: Citizen) -> str | None:
    try:
        template = MailTemplate.objects.get(name=WELCOME_SP_TEMPLATE_NAME)
    except MailTemplate.DoesNotExist:
        logger.warning("Mail template 'welcome sp' not found")
        return "Registration successful but we could not send the email"

    try:
        msg = EmailMessage(subject=template.name, body=template.html, to=[citizen.main_email])
        msg.content_subtype = "html"
        msg.send()
        SentEmail.objects.create(to=citizen.main_email, status=SentEmailStatus.SENT, template=template)
        return None
    except Exception as e:
        logger.exception("Failed to send welcome email to %s", citizen.main_email)
        SentEmail.objects.create(
            to=citizen.main_email,
            status=SentEmailStatus.FAILED,
            template=template,
            error=str(e),
        )
        return "Registration successful but we could not send the email"
