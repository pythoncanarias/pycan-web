#!/usr/bin/env python3

from .models import Ticket
from .tasks import send_ticket
from .tasks import send_ticket_canceled


def execute_trade(trade, payment_id):
    wl = trade.waiting_list
    old_ticket = trade.refund.ticket
    article = old_ticket.article
    new_ticket = Ticket(
        article=article,
        customer_name=wl.name,
        customer_surname=wl.surname,
        customer_email=wl.email,
        customer_phone=wl.phone,
        payment_id=payment_id,
        )
    new_ticket.save()
    old_ticket.invalid = True
    old_ticket.save()
    trade.finish(sucessful=True)
    send_ticket_canceled.delay(old_ticket)
    send_ticket.delay(new_ticket)
