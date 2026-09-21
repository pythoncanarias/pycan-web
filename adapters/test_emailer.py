#!/usr/bin/env python3

import pytest
from adapters import emailer

from django.core.mail import send_mail
from django.conf import settings


def test_create_message():
    msg = emailer.create_message(
        recipients=['euribates@gmail.com'],
        subject='[PyCanWeb] test asapters.emailer',
        template='emailer/test_emailer.md',
        from_email=settings.CONTACT_EMAIL,
        matraka="Matraka rules!",
        )
    assert msg.to == ['euribates@gmail.com']
    assert msg.from_email == settings.CONTACT_EMAIL
    assert msg.subject == '[PyCanWeb] test asapters.emailer'


@pytest.mark.slow
def test_simple_send():
    send_mail(
        "Subject here",
        "Here is the message.",
        "info@pythoncanarias.es",
        ["euribates@gmail.com"],
        )


@pytest.mark.slow
def test_send_email():
    msg = emailer.create_message(
        recipients=['euribates@gmail.com'],
        subject='[PyCanWeb] test asapters.emailer',
        template='emailer/test_emailer.md',
        from_email=settings.CONTACT_EMAIL,
        matraka="Matraka rules!",
        )
    result = msg.send()
    print('result:', result)
