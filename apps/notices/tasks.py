#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail
from python_http_client.exceptions import HTTPError

from django.template import Context, Template
from django.utils import timezone
from django_rq import job

from django.conf import settings
from apps.commons.filters import as_markdown


def create_notice_body(notice):
    kind = notice.kind
    context = Context({
        'kind': kind,
        'notice': notice,
        'member': notice.member,
        'user': notice.member.user,
    })
    template = Template(kind.template)
    return template.render(context)


def create_notice_message(notice):
    member = notice.member
    subject = f'[PythonCanarias] Aviso {notice.pk} para el socio nº {member.pk}'
    body = create_notice_body(notice)
    msg = Mail(
        from_email=Email(settings.CONTACT_EMAIL, settings.ASSOCIATION_NAME),
        subject=subject,
        to_email=Email(member.user.email),
        content=Content('text/html', as_markdown(body)))
    return msg


@job
def task_send_notice(notice):
    # Preconditions
    print('task_send_notice starts')
    if not notice.member.user.email:
        print("El usuario no tiene asignado email")
        return
    msg = create_notice_message(notice)
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    try:
        response = sg.client.mail.send.post(request_body=msg.get())
        notice.send_at = timezone.now()
        notice.reply_code = response.status_code
        if response.status_code >= 400:
            notice.rejected_at = timezone.now()
            notice.delivered_at = None
            notice.reject_message = response.body
        else:
            notice.rejected_at = None
            notice.delivered_at = timezone.now()
            notice.reject_message = None
        notice.save()
    except HTTPError as err:
        print("[ERROR]")
        notice.reply_code = err.status_code
        notice.rejected_at = timezone.now()
        notice.reject_message = str(err)
        notice.delivered_at = None
        notice.save()
