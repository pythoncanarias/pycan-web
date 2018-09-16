#!/usr/bin/env python
# coding=utf-8

import datetime
from unittest.mock import Mock
import pytest
from django.conf import settings

from . import tasks


@pytest.fixture
def test_ticket():
    event = Mock(
        get_long_start_date=Mock(return_value='Aquí va la fecha'),
        )
    event.name = 'Event name'
    category = Mock()
    category.name = 'Ticket type name'
    article = Mock(
        price=10.00,
        stock=20,
        )
    article.category = category
    article.event = event
    ticket = Mock(
        number=9,
        customer_name="Nombre del comprador",
        customer_surname='Apellidos comprador',
        customer_email='email@del.comprador.com',
        sold_at=datetime.datetime(2018, 10, 11, 22, 44, 00),
        keycode='18b0b618-7b9e-4857-9f01-39999424ee3f',
        )
    ticket.article = article
    return ticket


def test_create_ticket_pdf(test_ticket):
    fn = tasks.create_ticket_pdf(test_ticket, force=True)
    print(fn)
    assert test_ticket.keycode in fn


def test_send_message_smtplib():
    from email.message import EmailMessage
    import smtplib

    settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    message = 'Prueba de envio de correo desde django Buck Rogers'
    msg = EmailMessage()
    msg.set_content(message)
    msg['From'] = settings.EMAIL_HOST
    msg['subject'] = 'Prueba de envio desde smtplib'
    msg['To'] = 'euribates+test@gmail.com'
    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as s:
        s.ehlo()
        s.starttls()
        s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        s.send_message(msg)


def test_send_message_django():
    from django.core.mail import EmailMessage
    from django.core import mail

    print('Probando el envio desde Django/EmailMessage')
    subject = 'Prueba 2 de envio desde Django'
    txt = 'Don’t kill if you can wound, don’t wound if you can subdue,'  \
          ' don’t subdue, if you can pacify, and don’t raise a hand at all,' \
          ' until you’ve extended it.\n'  \
          '-- Wonder Woman'
    targets = ['euribates+test@gmail.com', ]
    settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    assert settings.EMAIL_HOST == 'smtp.gmail.com'
    assert settings.EMAIL_PORT == 587
    assert settings.EMAIL_HOST_USER == 'euribates@gmail.com'
    assert settings.EMAIL_HOST_PASSWORD == r'brc\Alerf656'
    assert settings.EMAIL_USE_TLS is True
    assert settings.EMAIL_USE_SSL is False
    with mail.get_connection() as connection:
        print('Connection:', connection)
        msg = EmailMessage(
            subject,
            txt,
            from_email=settings.EMAIL_HOST_USER,
            to=targets,
            connection=connection,
            )
        with open('/tmp/test.pdf', 'rb') as f:
            msg.attach(
                'temp.pdf',
                f.read(),
                'appilication/pdf'
            )
        msg.send(fail_silently=False)
    print('OK, mensaje enviado')


def test_send_ticket(test_ticket):
    tasks.send_ticket('euribates@gmail.com', test_ticket)


if __name__ == '__main__':
    pytest.main()
