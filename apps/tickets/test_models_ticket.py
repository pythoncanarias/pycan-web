#!/usr/bin/env python3

from datetime import datetime as DateTime
import os
import uuid

import pytest

from .models import Ticket


@pytest.fixture
def test_ticket():
    ticket = Ticket(
        number=-1,
        customer_name="Reed",
        customer_surname='Richards',
        customer_email='mr_fantastic@futurefoundation.com',
        sold_at=DateTime(2018, 10, 11, 22, 44, 00),
        keycode=uuid.UUID('d7d61e83-8518-4a85-8b5f-c4dc8ee00f19'),
        )
    return ticket


def test_ticket_get_qrcode_as_svg(test_ticket):
    '''Test ticket method get_qrcode_as_svg.
    '''
    svg_code = test_ticket.get_qrcode_as_svg()
    assert svg_code.startswith('<?xml')
    assert svg_code.strip().endswith('</svg>')


def test_get_tickets_dir(test_ticket):
    path = test_ticket.get_tickets_dir()
    assert 'temporal' in path
    assert 'tickets' in path
    assert os.path.isdir(path)


if __name__ == "__main__":
    pytest.main()
