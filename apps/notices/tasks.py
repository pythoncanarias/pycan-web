#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sendgrid
from django.conf import settings
from django.template import Context, Template
from django.utils import timezone
from django_rq import job
from python_http_client.exceptions import HTTPError
from sendgrid.helpers.mail import Content, Email, Mail

from apps.commons.filters import as_markdown
from apps.organizations.models import Organization


def create_notice_body(notice):
    kind = notice.kind
    context = Context(
        {
            'kind': kind,
            'notice': notice,
            'member': notice.member,
            'user': notice.member.user,
        }
    )
    template = Template(kind.template)
    return template.render(context)


def create_notice_message(notice):
    member = notice.member
    subject = notice.kind.description
    body = create_notice_body(notice)
    organization = Organization.load_main_organization()
    msg = Mail(
        from_email=Email(organization.email, organization.name),
        subject=subject,
        to_email=Email(member.email),
        content=Content('text/html', as_markdown(body)),
    )
    return msg


@job
def task_send_notice(notice):
    # Preconditions
    if not notice.member.email:
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
