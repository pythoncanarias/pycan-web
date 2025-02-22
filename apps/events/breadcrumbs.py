#!/usr/bin/env python3

from django.urls import reverse_lazy

from apps.commons.breadcrumbs import HOMEPAGE


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


def bc_next_events():
    return bc_root().step(
        'Últimos eventos',
        reverse_lazy('events:next'),
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
