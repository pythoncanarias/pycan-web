from django.urls import path

from . import views

app_name = 'about'


def tie(url_path, view_function, name=None):
    """Use the name of the function as the name of the url.

    Unlesss a different name were specified using the ``name`` parameter.
    """
    return path(url_path, view_function, name=name or view_function.__name__)


urlpatterns = [
    tie('', views.index),
    tie('us/', views.us),
    tie('join/', views.join),
    tie('board/', views.board),
    tie('history/', views.history),
    tie('allies/', views.allies),
    tie('faq/', views.faq_list, name='faq'),
    ]
