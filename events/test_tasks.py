#!/usr/bin/env python
# coding=utf-8

import datetime
from unittest.mock import Mock
import pytest

from . import tasks


    @pytest.fixture
    def ticket():
        event = Mock(
            name='Event name',
            get_long_start_date=Mock(),
            )

        ticket_type = Mock(
            event=event,
            name='Ticket type name',
            price=10,
            )

        ticket = Mock(
            ticket_type=ticket_type,
            name="Nombre del comprador",
            surname='Apellidos',
            email='euribates@gmail.com',
            sold_at=datetime.datetime(2018, 10, 11, 22, 44, 00),
            keycode='18b0b618-7b9e-4857-9f01-39999424ee3f',
            get_qrcode_url=Mock(
                return_value='http://www.parcan.es/art/escudo.png'
                ),
            )
        return ticket


def test_send_ticket(ticket):
    tasks.send_ticket(
        'euribates@gmail.com',
        ticket,
        )


if __name__ == '__main__':
    pytest.main()
