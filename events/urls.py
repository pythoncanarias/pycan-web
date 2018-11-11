from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('privacy/', views.privacy, name='privacy'),
    path('legal/', views.legal, name='legal'),  # aviso legal
    path('coc/', views.coc, name='coc'),
    path('coc/<language>/', views.coc, name='coc'),
    path('<slug:slug>/', views.detail_event, name='detail_event'),
    path(
        '<slug:slug>/waiting-list/',
        views.waiting_list,
        name='waiting_list',
        ),
    path(
        '<slug:slug>/waiting-list/accepted/',
        views.waiting_list_accepted,
        name='waiting_list_accepted',
        ),
    path(
        '<slug:slug>/refund/',
        views.refund,
        name='refund',
        ),
    path(
        '<slug:slug>/refund/accepted/<int:pk>/',
        views.refund_accepted,
        name='refund_accepted',
        ),
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
    path(
        'ticket/purchase/bought/<int:id_article>/',
        views.article_bought,
        name='article_bought',
        ),
    path(
        'ticket/purchase/<int:id_article>/',
        views.ticket_purchase,
        name='ticket_purchase',
        ),
]
