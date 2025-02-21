from django.urls import path

from . import views

app_name = 'legal'


def tie(url_path, view_function, name=None):
    """Use the name of the function as the name of the url.

    Unlesss a different name were specified using the ``name`` parameter.
    """
    return path(url_path, view_function, name=name or view_function.__name__)


urlpatterns = [
    tie('', views.legal_notice),
    tie('privacy_policy/', views.privacy_policy),
    tie('purchase_terms/', views.purchase_terms),
    tie('cookie_policy/', views.cookie_policy),
    tie('coc/', views.coc),
    tie('coc/es/', views.coc, name='coc_spanish'),
    tie('coc/en/', views.coc_english, name='coc_english'),
    ]
