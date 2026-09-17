from django.urls import path

from . import views

app_name = 'legal'

def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)

urlpatterns = [
    tie('', views.legal_notice),
    tie('privacy_policy/', views.privacy_policy),
    tie('purchase_terms/', views.purchase_terms),
    tie('cookie_policy/', views.cookie_policy),
    tie('coc/', views.coc),
    tie('coc/<language>/', views.coc),
    ]
