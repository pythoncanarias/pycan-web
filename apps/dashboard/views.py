#!/usr/bin/env python3

from django.shortcuts import render

from apps.certificates.models import Attendee
from apps.events.models import Event
from apps.jobs.models import JobOffer
from apps.members.models import Membership
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


def attendees(request, pk, *args, **kwargs):
    event = Event.load_event(pk)
    attendees = Attendee.objects.filter(event=event)
    return render(request, "dashboard/attendees.html", {
        'event': event,
        'attendees': attendees,
        })
