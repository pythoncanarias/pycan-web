from django.urls import include, path
from . import views

from . import models

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('buy/<int:id_ticket_type>/', views.buy_ticket, name='buy_ticket'),
    path('<slug:slug>', views.detail_event, name='detail_event'),
    path('ticket/<uuid:keycode>/', views.ticket_bought, name='ticket_bought'),
    path('ticket/test/', views.view_qr_code, name='qr_code'),
]
