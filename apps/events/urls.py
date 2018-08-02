from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('coc/', views.coc, name='coc'),
    path('buy/<int:id_ticket_type>/', views.buy_ticket, name='buy_ticket'),
    path('<slug:slug>', views.detail_event, name='detail_event'),
    path('ticket/<uuid:keycode>/', views.ticket_bought, name='ticket_bought'),
    path('ticket/test/', views.view_qr_code, name='qr_code'),
    path('ticket/<uuid:keycode>/pdf/', views.ticket_pdf, name='ticket_pdf'),
]
