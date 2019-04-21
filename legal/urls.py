from django.urls import path

from . import views

app_name = 'legal'

urlpatterns = [
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('legal_notice/', views.legal_notice, name='legal_notice'),
    path('purchase_terms/', views.purchase_terms, name='purchase_terms'),
    path('cookie_policy/', views.cookie_policy, name='cookie_policy'),
    path('coc/', views.coc, name='coc'),
    path('coc/<language>/', views.coc, name='coc'),
]
