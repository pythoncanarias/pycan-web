from django.urls import path

from . import views

app_name = 'dashboard'

def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('members/new/', views.new_member),
    tie('members/', views.active_members),
    ]
