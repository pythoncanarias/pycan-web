from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('privacy/', views.privacy, name='privacy'),
    path('coc/', views.coc, name='coc'),
    path('coc/<language>/', views.coc, name='coc'),
    path('<slug:slug>/', views.detail_event, name='detail_event'),
    path(
        '<slug:slug>/resend_ticket/',
        views.resend_ticket,
        name='resend_ticket',
        ),
    path(
        '<slug:slug>/resend_ticket/confirmation',
        views.resend_confirmation,
        name='resend_confirmation',
        ),
    path('<slug:slug>/buy/', views.buy_ticket, name='buy_ticket'),
    path('ticket/purchase/<int:id_article>/', views.ticket_purchase, name='ticket_purchase'),
    path('ticket/<uuid:keycode>/', views.article_bought, name='article_bought'),
    path('ticket/<int:pk>/qrcode/', views.ticket_qrcode, name='ticket_qrcode'),
]
