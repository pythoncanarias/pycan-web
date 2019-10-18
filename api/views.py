#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import traceback
from collections import defaultdict

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse

from events.models import Event
from locations.models import Venue
from members.models import Position

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


# Serializars


def serialize_venue_short(venue):
    return {
        'venue_id': venue.pk,
        'name': venue.name,
        'slug': venue.slug,
        'detail': reverse('api:detail_venue', args=[venue.slug]),
    }


def serialize_venue(venue):
    return {
        'vanue_id': venue.pk,
        'name': venue.name,
        'description': venue.description,
        'address': venue.address,
        'coords': {
            'lat': venue.latitude,
            'long': venue.longitude
        },
        'photo': venue.photo_url,
    }


def serialize_event_short(event):
    return {
        'event_id': event.pk,
        'hashtag': event.slug,
        'name': event.name,
        'active': event.active,
        'start': event.start_date.isoformat(),
        'detail': reverse('api:detail_event', args=[event.slug]),
    }


def serialize_event(event):
    return {
        'event_id': event.pk,
        'name': event.name,
        'full_url': event.get_full_url(),
        'active': event.active,
        'start_date': event.start_date.isoformat(),
        'short_description': event.short_description,
        'description': event.description,
        'venue': reverse('api:detail_venue', args=[event.venue.slug]),
        'speakers': reverse('api:list_speakers', args=[event.slug]),
        'talks': reverse('api:list_talks', args=[event.slug]),
        'tracks': reverse('api:list_tracks', args=[event.slug]),
        'tags': reverse('api:list_tags', args=[event.slug]),
        'sponsors': reverse('api:list_sponsors', args=[event.slug]),
    }


def serialize_speaker(event, speaker):
    return {
        'speaker_id': speaker.pk,
        'name': speaker.name,
        'surname': speaker.surname,
        'bio': speaker.bio,
        'photo': speaker.photo_url,
        'social': speaker.socials(),
        'talks': [serialize_talk(talk) for talk in speaker.talks(event)],
    }


def serialize_talk(talk):
    return {
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
    }


def serializer_sponsor(sponsor):
    return {
        'organization_id': sponsor.organization.pk,
        'name': sponsor.organization.name,
        'url': sponsor.organization.url,
        'logo': sponsor.organization.logo.url if sponsor.organization.logo else '',
        'category': str(sponsor.category),
        'role': str(sponsor.category.role),
    }


def serializer_staff(position):
    return {
        'position': position.get_position_display(),
        'first_name': position.member.user.first_name,
        'last_name': position.member.user.last_name,
        'email': position.member.user.email,
    }


@api
def status(request):
    return {
        "active":
            True,
        "version":
            settings.CURRENT_API_VERSION,
        "entry_points": [
            reverse('api:status'),
            reverse('api:list_venues'),
            reverse('api:active_events'),
            reverse('api:all_events'),
        ]
    }


@api
def list_staff_members(request):
    """List of active staff members."""
    return [
        serializer_staff(staff_member)
        for staff_member in Position.objects.filter(active=True).select_related('member__user')
    ]


@api
def list_venues(request):
    """List of all venues.
    """
    return [serialize_venue_short(venue) for venue in Venue.objects.all()]


@api
def detail_venue(request, slug):
    venue = Venue.objects.get(slug=slug)
    return serialize_venue(venue)


@api
def all_events(request):
    """Return a list with some data of all events, past, present or future'
    """
    events = Event.objects.all().order_by('-start_date')
    return [serialize_event_short(event) for event in events]


@api
def active_events(request):
    """Return a list with some data of active events (present or future)'
    """
    events = Event.objects.filter(active=True).order_by('start_date')
    return [serialize_event_short(event) for event in events]


@api
def detail_event(request, slug):
    """Details from event indicated, with URL pointing to more resources.
    """
    event = Event.get_by_slug(slug)
    return serialize_event(event)


@api
def list_speakers(request, slug):
    event = Event.get_by_slug(slug)
    speakers = event.speakers()
    return [serialize_speaker(event, speaker) for speaker in speakers]


@api
def list_talks(request, slug):
    event = Event.get_by_slug(slug)
    talks = [s for s in event.schedule.select_related('slot').order_by('slot__name') if s.slot.is_talk()]
    return [serialize_talk(talk) for talk in talks]


@api
def list_tracks(request, slug):
    event = Event.get_by_slug(slug)
    tracks = event.tracks()
    return [{'name': track.name, 'schedule': track.get_talks()} for track in tracks]


@api
def list_sponsors(request, slug):
    event = Event.get_by_slug(slug)
    sponsors = event.memberships.all().order_by('category__role__order')
    return [serializer_sponsor(sponsor) for sponsor in sponsors]

# TODO
@api
def list_tags(request, slug):
    return []
