from django.urls import path, re_path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^coc/((?P<language>\w+)/)?$', views.coc, name='coc'),
    path('buy/<int:id_ticket_type>/', views.buy_ticket, name='buy_ticket'),
    path('<slug:slug1>/<slug:slug2>/', views.detail_event, name='detail_event'),
    path('ticket/<uuid:keycode>/', views.ticket_bought, name='ticket_bought'),
    path('ticket/<int:pk>/qrcode/', views.ticket_qrcode, name='ticket_qrcode'),
    path('ticket/<uuid:keycode>/pdf/', views.ticket_pdf, name='ticket_pdf'),
]
