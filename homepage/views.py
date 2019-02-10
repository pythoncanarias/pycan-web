#!/usr/bin/env python

from django.shortcuts import render

from events.models import Event
from quotes.models import Quote


def homepage(request):
    return render(request, 'homepage/index.html', {
        'active_events': Event.objects.all().filter(active=True).count(),
        'quote': Quote.get_random_quote()
    })
