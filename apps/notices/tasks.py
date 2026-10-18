#!/usr/bin/env python3

from django.utils import timezone
from django_rq import job

from adapters.emailer import create_message, send_message
from apps.notices.models import Notice



@job
def task_send_notice(id_notice):
    notice = Notice.load_notice(id_notice)
    # Preconditions
    if not notice.member.email:
        print("El usuario no tiene asignado email")
        return
    try:
        msg = create_message(
            [notice.member.email],
            notice.kind.description,
            body_text=notice.message_text,
            notice=notice,
            kind=notice.kind,
            member=notice.member,
            )
        notice.reply_code = result = send_message(msg)
        if result:
            notice.send_at = timezone.now()
        else:
            notice.rejected_at = timezone.now()
    except Exception as err:
        notice.rejected_at = timezone.now()
        notice.reject_message = str(err)
        notice.delivered_at = None
    finally:
        notice.save()
