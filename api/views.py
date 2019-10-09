#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse

from events.models import Event
from locations.models import Venue


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
        return JsonResponse(response, json_dumps_params={'indent': 4})

    return wrapper


@api
def status(request):
    return {
        "active": True,
        "version": settings.CURRENT_API_VERSION,
        "entry_points": [
            reverse('api:status'),
            reverse('api:active_events'),
            reverse('api:all_events'),
            ]
        }


@api
def list_venues(request):
    """List of all venues.
    """
    return [
        {
            'venue_id': venue.pk,
            'name': venue.name,
            'slug': venue.slug,
            'detail': reverse('api:detail_venue', args=[venue.slug]),
        } for venue in Venue.objects.all()
        ]


@api
def detail_venue(request, slug):
    venue = Venue.objects.get(slug=slug)
    return {
        'vanue_id': venue.pk,
        'name': venue.name,
        'description': venue.description,
        'address': venue.address,
        'coords': {'lat': venue.latitude, 'long': venue.longitude},
        'photo': venue.photo_url,
        }


@api
def all_events(request):
    """Return a list with some data of all events, past, present or future'
    """
    events = Event.objects.all().order_by('-start_date')
    return [{
        'event_id': event.pk,
        'slug': event.slug,
        'name': event.name,
        'active': event.active,
        'start': event.start_date.isoformat(),
        'detail': reverse('api:detail_event', args=[event.slug]),
    } for event in events]


@api
def active_events(request):
    """Return a list with some data of active events (present or future)'
    """
    active_events = (
        Event.objects.all()
        .filter(active=True)
        .order_by('start_date')
        )
    return [{
        'event_id': event.pk,
        'slug': event.slug,
        'name': event.name,
        'start': event.start_date.isoformat(),
        'url': event.get_full_url(),
        'detail': reverse('api:detail_event', args=[event.slug]),
    } for event in active_events]


@api
def detail_event(request, slug):
    """Details from event indicated, with URL pointing to more resources.
    """
    event = Event.get_by_slug(slug)
    return {
        'id': event.pk,
        'name': event.name,
        'full_url': event.get_full_url(),
        'active': event.active,
        'start_date': event.start_date.isoformat(),
        'short_description': event.short_description,
        'venue': reverse('api:detail_venue', args=[event.venue.slug]),
        'speakers': reverse('api:list_speakers', args=[event.hashtag]),
        'talks': reverse('api:list_talks', args=[event.hashtag]),
        'tracks': reverse('api:list_tracks', args=[event.hashtag]),
    }


@api
def list_speakers(request, slug):
    event = Event.get_by_slug(slug)
    speakers = event.speakers()
    return [
        {
            'id': speaker.pk,
            'name': speaker.name,
            'surname': speaker.surname,
            'bio': speaker.bio,
            'photo': speaker.photo_url,
            'social': speaker.socials(),
            'talks': speaker.talks(),
        } for speaker in speakers
    ]


@api
def list_talks(request, slug):
    event = Event.get_by_slug(slug)
    talks = [
        s for s in event
        .schedule
        .select_related('slot')
        .order_by('slot__name')
        if s.slot.is_talk()
        ]
    return [
        {
            'talk_id': talk.pk,
            'name': talk.slot.name,
            'description': talk.slot.description,
            'repo': talk.slot.repo,
            'tags': talk.slot.get_tags(),
            'track': talk.track_name(),
            'start': talk.start.strftime('%H:%M'),
            'end': talk.end.strftime('%H:%M'),
            'level': talk.slot.get_level(),
            'speakers': talk.get_speakers(),
        } for talk in talks
    ]


@api
def list_tracks(request, slug):
    event = Event.get_by_slug(slug)
    tracks = event.tracks()
    return [
        {'name': track.name, 'schedule': track.get_talks()}
        for track in tracks
        ]
