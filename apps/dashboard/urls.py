
from django.urls import path, register_converter

from . import views


app_name = 'dashboard'


def tie(ruta, vista):
    return path(ruta, vista, name=vista.__name__)


urlpatterns = [
    tie('', views.index, name='index'),
    tie('certificates/', views.certificates),
    tie('certificates/issue/', views.issue_certificates),
    tie('demo/', views.demo),
    ]
