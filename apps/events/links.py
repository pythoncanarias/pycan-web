#!/usr/bin/env python3

from django.urls import reverse_lazy


def to_event_detail(slug):
    return reverse_lazy('events:detail_event', kwargs={'event': slug})


def to_proposal_received(event):
    return reverse_lazy("events:proposal_received", kwargs={
        "event": event,
        })


def to_speakers(event):
    return reverse_lazy("events:speakers", kwargs={
        "event": event,
        })


def to_talks(event):
    return reverse_lazy("events:talks", kwargs={
        "event": event,
        })


def to_event_place(event):
    return reverse_lazy("events:event_place", kwargs={
        "event": event,
        })


def to_waiting_list(event):
    return reverse_lazy("events:waiting_list", kwargs={
        'event': event,
        })


def to_refund(event):
    return reverse_lazy("events:refund", kwargs={
        'event': event,
        })


def to_refund_accepted(event, pk):
    return reverse_lazy("events:refund_accepted", kwargs={
        'event': event,
        'pk': pk,
        })


def to_ticket_purchase(id_article):
    id_article = int(id_article)
    return reverse_lazy('events:ticket_purchase', kwargs={'id_article': id_article})


def to_article_bought(id_article):
    id_article = int(id_article)
    return reverse_lazy('events:article_bought', kwargs={
        'pk': id_article,
        })


def to_waiting_list_accepted(event):
    return reverse_lazy('events:waiting_list_accepted', kwargs={
        'event': event,
        })


def to_resend_ticket(event):
    return reverse_lazy('events:resend_ticket', kwargs={
        'event': event,
        })


def to_resend_confirmation(event):
    return reverse_lazy('events:resend_confirmation', kwargs={
        'event': event,
        })


def to_raffle(event):
    return reverse_lazy('events:raffle', kwargs={
        'event': event,
        })


def to_raffle_gifts(event):
    return reverse_lazy('events:raffle_gifts', kwargs={
        'event': event,
        })


def to_raffle_results(event):
    return reverse_lazy('events:raffle_results', kwargs={
        'event': event,
        })


def to_buy_ticket(event):
    return reverse_lazy('events:buy_ticket', kwargs={
        'event': event,
        })


