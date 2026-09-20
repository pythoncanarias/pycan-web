from django.urls import path

from . import views

app_name = 'members'


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.homepage),
    tie("membership/", views.membership),
    tie("password/change/", views.password_change),
    tie("address/change/", views.address_change),
    tie("login/", views.member_login),
    tie("logout/", views.member_logout),
    ]
