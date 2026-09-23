#!/usr/bin/env python3

import os
from datetime import datetime as Date
from datetime import datetime as DateTime
from decimal import Decimal

import pytest
from django.core.mail import EmailMessage

from apps.events.models import Event
from apps.tickets.models import Article, Ticket, TicketCategory

from . import tasks


@pytest.fixture
def test_ticket():
    event = Event(
        name='Text Event',
        description='Event for tests',
        short_description='Event for tests',
        hashtag='test_event',
        active=True,
        start_date=Date.today(),
        )
    category = TicketCategory(
        name='Article test category',
        slug='article_test_category',
        )
    article = Article(
        event=event,
        category=category,
        price=Decimal('10.0'),
        stock=99,
        )
    ticket = Ticket(
        number=1,
        article=article,
        customer_name="Tabitha",
        customer_surname="Smith",
        customer_email='boomboom@villiansunited.com',
        sold_at=DateTime(2018, 10, 11, 22, 44, 00),
        keycode='18b0b618-7b9e-4857-9f01-39999424ee3f',
        )
    return ticket


def test_get_qrcode_as_svg(test_ticket):
    svg_code = test_ticket.get_qrcode_as_svg('This is a test')
    assert svg_code.startswith('<?xml')
    assert svg_code.strip().endswith('</svg>')


def test_get_tickets_dir(test_ticket):
    path = test_ticket.get_tickets_dir()
    assert 'temporal' in str(path)
    assert 'tickets' in str(path)
    assert os.path.isdir(path)


@pytest.mark.slow
@pytest.mark.django_db
def test_create_ticket_message(test_ticket):
    msg = tasks.create_ticket_message(test_ticket)
    assert isinstance(msg, EmailMessage)


if __name__ == '__main__':
    pytest.main()
