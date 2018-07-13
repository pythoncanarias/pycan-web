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
        return render(request, 'events/event.html', {
            'event': events.first()
            })
    else:
        return render(request, 'events/list-events.html', {
            'events': events.all()
            })
