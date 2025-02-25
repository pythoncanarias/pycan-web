from django.urls import path

from . import views


app_name = 'debug'


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('vars/', views.context_processor_vars),
    tie('settings/', views.settings),
    ]
