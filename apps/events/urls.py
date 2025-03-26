from django.urls import path, register_converter

from . import views
from . import converters

app_name = 'events'


def tie(url_path, view_function, name=None):
    """Use the name of the function as the name of the url.

    Unlesss a different name were specified using the ``name`` parameter.
    """
    return path(url_path, view_function, name=name or view_function.__name__)


register_converter(converters.EventConverter, 'event')

urlpatterns = [
    tie('', views.index),
    tie('next/', views.next_event),
    tie('lastest/', views.last_events),
    tie('archive/', views.past_events),
    tie('<event:event>/', views.detail_event),
    tie('<event:event>/speakers/', views.speakers),
    tie('<event:event>/talks/', views.talks),
    tie('<event:event>/cfp/', views.call_for_papers),
    tie('<event:event>/cfp/thanks', views.proposal_received),
    tie('<event:event>/waiting-list/', views.waiting_list),
    tie('<event:event>/waiting-list/accepted/', views.waiting_list_accepted),
    tie('<event:event>/refund/', views.refund),
    tie('<event:event>/refund/accepted/<int:pk>/', views.refund_accepted),
    tie('<event:event>/raffle/', views.raffle),
    tie('<event:event>/raffle/gifts/', views.raffle_gifts),
    tie('<event:event>/raffle/results/', views.raffle_results),
    tie('<event:event>/raffle/<int:pk>/', views.raffle_gift),
    tie('<event:event>/raffle/<int:pk>/match/', views.raffle_gift_match),
    tie('<event:event>/raffle/close/', views.close_raffle),

    tie('<event:event>/buy/', views.buy_ticket),
    tie('ticket/purchase/<int:id_article>/', views.ticket_purchase),
    # ----[ por aqui ]--
    tie('<event:event>/resend_ticket/', views.resend_ticket),
    tie('<event:event>/resend_ticket/confirmation/', views.resend_confirmation),
    tie('ticket/purchase/bought/<int:pk>/', views.article_bought),
    # no credit card
    tie('ticket/purchase/<int:id_article>/nocc/', views.ticket_purchase_nocc),
    ]
