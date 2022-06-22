from django.urls import path, register_converter

from . import views
from .converters import LabelConverter

app_name = 'learn'

register_converter(LabelConverter, 'label')

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'labels/<label:label>/',
        views.resources_by_label,
        name='resources_by_label',
    ),
]
