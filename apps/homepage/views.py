#!/usr/bin/env python

from django.shortcuts import render

from apps.events.models import Event
from apps.quotes.models import Quote
from apps.jobs.models import JobOffer


def homepage(request):
    return render(request, 'homepage/index.html', {
        'active_events': Event.objects.all().filter(active=True).count(),
        'quote': Quote.get_random_quote(),
        'jobs_count': JobOffer.actives.count(),
    })
