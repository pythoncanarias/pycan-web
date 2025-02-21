from django.urls import path

from . import views

app_name = 'members'


def tie(url_path, view_function, name=None):
    """Use the name of the function as the name of the url.

    Unlesss a different name were specified using the ``name`` parameter.
    """
    return path(url_path, view_function, name=name or view_function.__name__)


urlpatterns = [
    tie("", views.homepage),
    tie("profile/", views.profile),
    tie("membership/", views.view_membership, name="membership"),
    tie("password/change/", views.password_change),
    tie("address/change/", views.address_change),
    tie("login/", views.member_login, name="login"),
    tie("logout/", views.member_logout, name="logout"),
    tie('join/', views.join),
    ]
