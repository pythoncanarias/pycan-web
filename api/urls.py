from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('v1/status', views.status, name='status'),
    path('v1/events', views.list_events, name='events'),
    path('v1/events/<slug>', views.detail_event, name='detail_event'),
]
