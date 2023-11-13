from django.urls import path

from . import views


app_name = 'dashboard'


def tie(ruta, vista):
    return path(ruta, vista, name=vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('members/', views.list_members),
    tie('certificates/', views.list_certificates),
    tie('certificates/all/', views.all_certificates),
    tie('certificates/<int:id_certificate>/', views.view_certificate),
    tie('certificates/<int:id_certificate>/issue/', views.issue_certificates),
    tie(
        'certificates/<int:id_certificate>/issue/<int:id_attendee>/',
        views.issue_certificate_attendee,
        ),
    tie('demo/', views.demo),
    ]
