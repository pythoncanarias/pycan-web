from django.urls import path

from . import views


app_name = 'api'


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('v1/status/', views.status),

    # organization
    tie('v1/organization/staff/', views.list_staff_members),
    # Venues
    tie('v1/venues/', views.list_venues),
    tie('v1/venues/<slug>/', views.detail_venue),
    # Events
    tie('v1/events/', views.active_events),
    tie('v1/events/all/', views.all_events),
    tie('v1/events/<slug>/', views.detail_event),
    tie('v1/events/<slug>/speakers/', views.list_speakers),
    tie('v1/events/<slug>/talks/', views.list_talks),
    tie('v1/events/<slug>/tracks/', views.list_tracks),
    tie('v1/events/<slug>/sponsors/', views.list_sponsors),
    # tags
    tie('v1/tags/', views.list_tags),
    # Quotes
    tie('v1/quotes/', views.random_quote),
    ]
