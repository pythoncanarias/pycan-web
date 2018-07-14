#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from . import models

def index(request):
    events = models.Event.objects.filter(active=True)
    num_events = events.count()
    if num_events == 0:
        return render(request, 'events/no-events.html')
    if num_events == 1:
        event = events.first()
        ticket_types = event.ticket_types.all().order_by('release_at')
        num_options = ticket_types.count()
        return render(request, 'events/event.html', {
            'event': event,
            'ticket_types': ticket_types,
            })
    else:
        return render(request, 'events/list-events.html', {
            'events': events.all()
            })

def detail_event(request, slug):
    from django.http import HttpResponse
    return HttpResponse('ok' + slug)


def buy_ticket(request, id_ticket_type):
    ticket_type = models.TicketType.objects.select_related('event').get(pk=id_ticket_type)
    event = ticket_type.event
    return render(request, 'events/buy_ticket.html', {
        'event': event,
        'ticket_type': ticket_type,
        })
