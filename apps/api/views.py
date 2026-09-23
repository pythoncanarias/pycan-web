#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import traceback

from django.conf import settings
from django.http import JsonResponse
from django.urls import get_resolver

from apps.events.models import Event
from apps.locations.models import Venue
from apps.members.models import Position
from apps.quotes.models import Quote
from apps.schedule.models import SlotTag

from . import serializers


def all_api_entrypoints():
    root = get_resolver()
    base_url, api_selector = root.namespace_dict['api']
    for url_pattern in api_selector.url_patterns:
        yield f'/{base_url}{url_pattern.pattern}'


# API decorator


def api(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = {'status': 'ok'}
        try:
            result = func(*args, **kwargs)
            try:
                length = len(result)
                response['length'] = length
            except TypeError:
                pass
            response['result'] = result
        except Exception as err:
            response['status'] = 'error'
            response['message'] = str(err)
            response['traceback'] = traceback.format_exc()
        return JsonResponse(response, json_dumps_params={'indent': 4})

    return wrapper


@api
def status(request):
    return {
        "active":
            True,
        "version":
            settings.CURRENT_API_VERSION,
        "entry_points": list(all_api_entrypoints()),
        }


@api
def list_staff_members(request):
    """List of active staff members."""
    return [
        serializers.as_staff(staff_member)
        for staff_member
        in Position.objects.actives()
        ]


@api
def list_venues(request):
    """List of all venues.
    """
    return [
        serializers.as_venue_short(venue)
        for venue in Venue.objects.all()
        ]


@api
def detail_venue(request, slug):
    """Detalles de un edificio o institución.
    """
    venue = Venue.objects.get(slug=slug)
    return serializers.as_venue(venue)


@api
def all_events(request):
    """List of all events.

    Returns a list with some data of all events, past,
    present or future.
    """
    events = Event.objects.all().order_by('-start_date')
    return [
        serializers.as_event_short(event)
        for event in events
        ]


@api
def active_events(request):
    """List of active events.

    Return a list with some data of active
    events (present or future).'
    """
    events = Event.objects.filter(active=True).order_by('start_date')
    return [serializers.as_event_short(event) for event in events]


@api
def detail_event(request, slug):
    """Details from event indicated, with URL pointing to more resources.
    """
    event = Event.get_by_slug(slug)
    return serializers.as_event(event)


@api
def list_speakers(request, slug):
    event = Event.get_by_slug(slug)
    speakers = event.speakers()
    return [
        serializers.as_speaker(event, speaker)
        for speaker in speakers
        ]


@api
def list_talks(request, slug):
    event = Event.get_by_slug(slug)
    talks = (
        s for s in event.schedule
            .select_related('slot')
            .order_by('slot__name')
        if s.slot.is_talk()
    )
    return [
        serializers.as_talk(talk)
        for talk in talks
        ]


@api
def list_tracks(request, slug):
    """Lista de tracks.

    Para un evento dado, devuelve la list de todas
    las secciones o tracks en las que se organiza
    el mismo.
    """
    event = Event.get_by_slug(slug)
    return [
        {
        'name': track.name,
        'schedule': track.get_talks(event),
        }
        for track in event.tracks()
        ]


@api
def list_sponsors(request, slug):
    event = Event.get_by_slug(slug)
    sponsors = event.memberships.all().order_by('category__role__order')
    return [serializers.as_sponsor(sponsor) for sponsor in sponsors]

@api
def random_quote(request):
    """Devuelve una cita al azar.

    Se utiliza de forma dinámica en la página principal.
    """
    quote = Quote.get_random_quote()
    return serializers.as_quote(quote)


@api
def list_tags(request):
    tags = SlotTag.objects.all().order_by('description')
    return [
        serializers.as_tag(tag)
        for tag in tags
        ]

