#!/usr/bin/env python

from django.shortcuts import render

from django.conf import settings

from apps.events.models import Event
from apps.quotes.models import Quote
from apps.jobs.models import JobOffer


def homepage(request):
    return render(request, 'homepage/index.html', {
        'active_events': Event.objects.all().filter(active=True),
        'quote': Quote.get_random_quote(),
        'jobs_count': JobOffer.actives.count(),
        'random_quote_interval': settings.RANDOM_QUOTE_INTERVAL,
    })
