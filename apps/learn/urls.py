from django.urls import path, register_converter

from . import views
from .converters import LabelConverter

app_name = 'learn'

register_converter(LabelConverter, 'label')


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('labels/<label:label>/', views.resources_by_label),
    ]
