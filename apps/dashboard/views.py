#!/usr/bin/env python3

from django.shortcuts import render
from apps.events.models import Event
from apps.members.models import Membership
from apps.jobs.models import JobOffer
from apps.quotes.models import Quote


def index(request, *args, **kwargs):
    return render(request, 'dashboard/index.html', {
        'title': 'Dashboard',
        'num_members': Membership.num_active_members(),
        'num_events': Event.objects.count(),
        'num_jobs': JobOffer.actives.count(),
        'num_quotes': Quote.objects.count(),
        })


def demo(request):
    return render(request, 'dashboard/demo.html', {
        'title': 'Dashboard',
        })


def certificates(request):
    events = Event.objects.all()
    return render(request, "dashboard/certificates.html", {
        'events': events,
        'num_events': events.count(),
        })
