from django.urls import path

from . import views


app_name = 'dashboard'


def tie(ruta, vista):
    return path(ruta, vista, name=vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('members/', views.list_members),
    tie('events/', views.list_events),
    tie('certificates/', views.list_certificates),
    tie('certificate/<int:id_certificate>/', views.view_certificate),
    tie('attendees/all/', views.all_attendees),
    tie('attendees/pending/', views.pending_attendees),
    tie('attendees/<int:id_attendee>/issue/', views.issue_attendee),
    ]
