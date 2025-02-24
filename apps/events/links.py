#!/usr/bin/env python3

from django.urls import reverse_lazy


def event_detail(slug):
    return reverse_lazy('events:detail_event', kwargs={'slug': slug})


def to_proposal_received(event):
    return reverse_lazy("events:proposal_received", kwargs={
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


def ticket_purchase(id_article):
    id_article = int(id_article)
    return reverse_lazy('events:ticket_purchase', kwargs={'id_article': id_article})


def article_bought(id_article):
    id_article = int(id_article)
    return reverse_lazy('events:article_bought', kwargs={'id_article': id_article})


def waiting_list_accepted(slug):
    return reverse_lazy('events:waiting_list_accepted', kwargs={
        'slug': slug,
        })


def refund(slug):
    return reverse_lazy('events:refund', kwargs={
        'slug': slug,
        })


def refund_accepted(slug, pk):
    return reverse_lazy('events:refund_accepted', kwargs={
        'slug': slug,
        'pk': pk,
        })
