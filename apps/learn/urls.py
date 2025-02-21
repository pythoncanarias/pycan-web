from django.urls import path, register_converter

from . import views
from .converters import LabelConverter

app_name = 'learn'

register_converter(LabelConverter, 'label')


def tie(url_path, view_function, name=None):
    """Use the name of the function as the name of the url.

    Unlesss a different name were specified using the ``name`` parameter.
    """
    return path(url_path, view_function, name=name or view_function.__name__)


urlpatterns = [
    tie('', views.index, name='index'),
    tie('labels/<label:label>/', views.resources_by_label),
    ]
