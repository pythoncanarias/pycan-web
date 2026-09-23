# Api serializars

from django.urls import reverse

def as_venue_short(venue):
    return {
        'venue_id': venue.pk,
        'name': venue.name,
        'slug': venue.slug,
        'detail': reverse('api:detail_venue', args=[venue.slug]),
    }


def as_venue(venue):
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


def as_event_short(event):
    return {
        'event_id': event.pk,
        'hashtag': event.slug,
        'name': event.name,
        'active': event.active,
        'start': event.start_date.isoformat(),
        'detail': reverse('api:detail_event', args=[event.slug]),
    }


def as_event(event):
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


def as_speaker(event, speaker):
    return {
        'speaker_id': speaker.pk,
        'name': speaker.name,
        'surname': speaker.surname,
        'bio': speaker.bio,
        'photo': speaker.photo_url,
        'social': speaker.socials(),
        'talks': [as_talk(talk) for talk in speaker.talks(event)],
    }


def as_talk(talk):
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


def as_sponsor(sponsor):
    return {
        'organization_id': sponsor.organization.pk,
        'name': sponsor.organization.name,
        'url': sponsor.organization.url,
        'logo': sponsor.organization.logo.url if sponsor.organization.logo else '',
        'category': str(sponsor.category),
        'role': str(sponsor.category.role),
    }


def as_staff(position):
    return {
        'position': position.get_position_display(),
        'first_name': position.member.user.first_name,
        'last_name': position.member.user.last_name,
        }


def as_quote(quote):
    return {
        'text': quote.text,
        'author': quote.author.name + ' ' + quote.author.surname,
    }


def as_tag(tag):
    return {
        'id_tag': tag.pk,
        'slug': tag.slug,
        'description': tag.description,
        }
