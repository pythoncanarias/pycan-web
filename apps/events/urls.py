from django.urls import path, register_converter

from . import views
from . import converters

app_name = 'events'

register_converter(converters.EventConverter, 'event')

urlpatterns = [
    path('', views.index, name='index'),
    path('next/', views.next, name='next'),
    path('archive/', views.past_events, name='past_events'),
    path('<slug:slug>/', views.detail_event, name='detail_event'),
    path('<event:event>/cfp/', views.call_for_papers, name='cfp'),
    path('<event:event>/cfp/thanks', views.proposal_received, name='thanks'),
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
        '<slug:slug>/trade/<uuid:sell_code>/<uuid:buy_code>/',
        views.trade,
        name='trade',
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
    path(
        'ticket/purchase/<int:id_article>/nocc/',  # no credit card
        views.ticket_purchase_nocc,
        name='ticket_purchase_nocc',
    ),
    path('<slug:slug>/raffle/', views.raffle, name='raffle'),
    path(
        '<slug:slug>/raffle/<int:gift_id>/',
        views.raffle_gift,
        name='raffle_gift',
    ),
    path(
        '<slug:slug>/raffle/<int:gift_id>/match/',
        views.raffle_gift,
        {'match': True},
        name='raffle_gift_match',
    ),
    path(
        '<slug:slug>/raffle/results/',
        views.raffle_results,
        name='raffle_results',
    ),
]
