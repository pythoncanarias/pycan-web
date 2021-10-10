#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('v1/status/', views.status, name='status'),

    # organization
    path('v1/organization/staff/', views.list_staff_members, name='list_staff_members'),
    # Venues
    path('v1/venues/', views.list_venues, name='list_venues'),
    path('v1/venues/<slug>/', views.detail_venue, name='detail_venue'),
    # Events
    path('v1/events/<slug>/speakers/', views.list_speakers, name='list_speakers'),
    path('v1/events/<slug>/talks/', views.list_talks, name='list_talks'),
    path('v1/events/<slug>/tracks/', views.list_tracks, name='list_tracks'),
    path('v1/events/<slug>/sponsors/', views.list_sponsors, name='list_sponsors'),
    path('v1/events/<slug>/tags/', views.list_tags, name='list_tags'),
    path('v1/events/<slug>/', views.detail_event, name='detail_event'),
    path('v1/events/all/', views.all_events, name='all_events'),
    path('v1/events/', views.active_events, name='active_events'),
    # Quotes
    path('v1/quotes/', views.quote, name='quote'),
]
