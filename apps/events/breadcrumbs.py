#!/usr/bin/env python3

from django.urls import reverse_lazy

from apps.commons.breadcrumbs import HOMEPAGE
from . import links


def bc_root():
    return HOMEPAGE.step(
        'Eventos',
        reverse_lazy('events:index'),
        )


def bc_event(event):
    return bc_root().step(
        str(event),
        reverse_lazy("events:detail_event", kwargs={
            'slug': event.slug,
            }),
        )


def bc_event_cfp(event):
    return bc_event(event).step(
        'Call for papers',
        reverse_lazy("events:call_for_papers", kwargs={
            'event': event,
            }),
        )


def bc_waiting_list(event):
    return bc_event(event).step(
        'Lista de espera',
        links.to_waiting_list(event),
        )


def bc_refund(event):
    return bc_event(event).step(
        'Solicitud de devolución',
        links.to_refund(event),
        )


def bc_refund_accepted(event, pk):
    return bc_refund(event).step(
        'Solicitud admitida',
        links.to_refund_accepted(event, pk),
        )


def bc_next_event():
    return bc_root().step(
        'Últimos eventos',
        reverse_lazy('events:next_event'),
        )


def bc_resend_ticket(event):
    return bc_event(event).step(
        'Reenviar entrada',
        links.to_resend_ticket(event),
        )


def bc_resend_confirmation(event):
    return bc_resend_ticket(event).step(
        'Entrada reenviada',
        links.to_resend_confirmation(event),
        )


def bc_last_events():
    return bc_root().step(
        'Últimos eventos',
        reverse_lazy('events:index'),
        )


def bc_past_events():
    return bc_root().step(
        'Archivo de eventos',
        reverse_lazy('events:past_events'),
        )


def bc_proposal_received(event):
    return bc_event_cfp(event).step(
        'Propuesta recibida',
        links.to_proposal_received(event),
        )


def bc_raffle(event):
    return bc_event(event).step(
        'Sorteo',
        links.to_raffle(event),
        )


def bc_raffle_gifts(event):
    return bc_raffle(event).step(
        'Regalos',
        links.to_raffle_gifts(event),
        )


def bc_raffle_results(event):
    return bc_raffle(event).step(
        'Resultados',
        links.to_raffle_results(event),
        )


def bc_buy_ticket(event):
    return bc_event(event).step(
        'Comprar entrada',
        links.to_buy_ticket(event),
        )


def bc_article_bought(article):
    return bc_event(article.event).step(
        'Articulo {article} comprado',
        links.at_article_bought(article),
        )


def bc_payment_error(event):
    return bc_event(event).step(
        'Error en la compra de una entrada',
        links.at_buy_article(event),
        )
