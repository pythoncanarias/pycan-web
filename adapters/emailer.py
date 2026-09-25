#!/usr/bin/env python3

from email.message import EmailMessage

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils import timezone

from apps.commons.filters import as_markdown


def create_message(
        recipients: list,
        subject: str,
        template: str,
        from_email: str | None = None,
        attachments: list | None = None,
        **kwargs,
        ) -> EmailMessage:
    assert len(recipients) > 0, "No se han indicado destinatarios"
    if from_email is None:
        from_email = settings.CONTACT_EMAIL
    _template = get_template(template)
    context = kwargs.copy()
    context.update({
        'current_datetime': timezone.now(),
        'to_email': ', '.join(recipients),
        'recipients': recipients,
        'template': template,
        'subject': subject,
        'from_email': from_email,
        })
    plain_body_text = _template.render(context)
    msg = EmailMultiAlternatives(
        subject=subject,
        body=plain_body_text,
        from_email=from_email,
        to=recipients,
        )
    # According to RFC 2046, the last part of a multipart message, in
    # this case the HTML message, is best and preferred.
    html_content = as_markdown(plain_body_text)
    msg.attach_alternative(html_content, "text/html")
    if attachments:
        for attachment in attachments:
            with open(attachment, 'rb') as f:
                data = f.read()
                msg.attach(attachment, data)
    return msg


def send_message(msg):
    return msg.send()
