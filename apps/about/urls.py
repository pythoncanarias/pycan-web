from django.urls import path

from . import views

app_name = 'about'


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.index),
    tie('us/', views.us),
    tie('join/', views.join),
    tie('join/method/', views.join_method),
    tie('history/', views.history),
    tie('allies/', views.allies),
    tie('faq/', views.faq_list, name="faq"),
]
