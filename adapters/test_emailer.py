#!/usr/bin/env python3

import pytest
from django.conf import settings

from adapters import emailer


def test_create_message():
    msg = emailer.create_message(
        recipients=['euribates@gmail.com'],
        subject='[PyCanWeb] test adapters.emailer',
        template='emailer/test_emailer.md',
        matraka="Matraka rules!",
        )
    assert msg.to == ['euribates@gmail.com']
    assert msg.from_email == settings.CONTACT_EMAIL
    assert msg.subject == '[PyCanWeb] test adapters.emailer'


def test_simple_send():
    msg = emailer.create_message(
        ["euribates@gmail.com"],
        "Subject here",
        body_text="Hola, mundo\n",
        from_email='info@pythoncanarias.es',
        )

    emailer.send_message(msg)


def test_send_email_using_templates():
    msg = emailer.create_message(
        ['euribates@gmail.com'],
        '[PyCanWeb] test asapters.emailer',
        template='emailer/test_emailer.md',
        from_email=settings.CONTACT_EMAIL,
        matraka="Matraka rules!",
        )
    emailer.send_message(msg)
