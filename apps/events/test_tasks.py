#!/usr/bin/env python3
# coding=utf-8

from datetime import datetime as DateTime
import os
from unittest.mock import Mock

import pytest
from django.core.mail import EmailMessage

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
        customer_email='euribates@gmail.com',
        sold_at=DateTime(2018, 10, 11, 22, 44, 00),
        keycode='18b0b618-7b9e-4857-9f01-39999424ee3f',
        )
    ticket.article = article
    return ticket


def test_get_qrcode_as_svg():
    svg_code = tasks.get_qrcode_as_svg('This is a test')
    assert svg_code.startswith('<?xml')
    assert svg_code.strip().endswith('</svg>')


def test_get_tickets_dir():
    path = tasks.get_tickets_dir()
    assert 'temporal' in path
    assert 'tickets' in path
    assert os.path.isdir(path)


def test_create_ticket_pdf(test_ticket):
    path = tasks.create_ticket_pdf(test_ticket)
    assert test_ticket.keycode in path
    assert path.endswith('.pdf')
    assert os.path.exists(path)


def test_create_ticket_message(test_ticket):
    msg = tasks.create_ticket_message(test_ticket)
    assert isinstance(msg, EmailMessage)


def test_send_ticket(test_ticket):
    tasks.send_ticket(test_ticket)


if __name__ == '__main__':
    pytest.main()
