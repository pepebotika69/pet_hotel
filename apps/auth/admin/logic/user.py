import logging

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template import Context, Template

from apps.embassy.defs.citizen_register import GOT_ACCESS_WITH_LOGIN_TEMPLATE_NAME
from apps.mail.models import MailTemplate, SentEmail, SentEmailStatus

logger = logging.getLogger(__name__)


def send_login_after_registration_email(user: User) -> str | None:
    try:
        template = MailTemplate.objects.get(name=GOT_ACCESS_WITH_LOGIN_TEMPLATE_NAME)
    except MailTemplate.DoesNotExist:
        logger.warning("Mail template '%s' not found", GOT_ACCESS_WITH_LOGIN_TEMPLATE_NAME)
        return "User created but we could not send the access email"

    try:
        html = Template(template.html).render(Context({"username": user.username}))
        msg = EmailMessage(subject=template.name, body=html, to=[user.email])
        msg.content_subtype = "html"
        msg.send()
        SentEmail.objects.create(to=user.email, status=SentEmailStatus.SENT, template=template)
        return None
    except Exception as e:
        logger.exception("Failed to send access email to %s", user.email)
        SentEmail.objects.create(
            to=user.email,
            status=SentEmailStatus.FAILED,
            template=template,
            error=str(e),
        )
        return "User created but we could not send the access email"
