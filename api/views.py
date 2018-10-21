from django.http import HttpResponse
import json
import functools

CURRENT_API_VERSION = 1

from events.models import Event


def api(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = {'status': 'ok'}
        try:
            result = func(*args, **kwargs)
            response['result'] = result
        except Exception as err:
            response['status'] = 'error'
            response['message'] = str(err)
        return HttpResponse(
            json.dumps(response, indent=4),
            content_type='application/json',
            )

    return wrapper


@api
def status(request):
    return {
        "active": True,
        "version": CURRENT_API_VERSION,
        }


@api
def list_events(request):
    active_events = Event.objects.all().filter(active=True).order_by('start_date')
    return [
        dict(
            slug=e.slug,
            name=e.name,
            start=e.start_date.isoformat(),
            ) 
        for e in active_events
        ]


@api
def detail_event(request, slug):
    event = Event.objects.get(slug=slug)
    tracks = event.tracks()
    return {
        'id': event.pk,
        'name': event.name,
        'active': event.active,
        'start_date': event.start_date.isoformat(),
        'short_description': event.short_description,
        'url': event.get_full_url(),
        'tracks': [
            {
                'track_id': t.pk,
                'order': t.order,
                'name': t.name,
                'talks': t.get_talks(),
            } for t in tracks
            ],
        }

