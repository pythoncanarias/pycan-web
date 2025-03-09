from datetime import datetime as DateTime
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import redirect, render
import stripe

from . import breadcrumbs
from . import forms
from . import links
from . import models
from . import stripe_utils
from . import tasks
from apps.organizations.models import Organization
from apps.tickets.models import Article, Gift, Ticket


logger = logging.getLogger(__name__)


def index(request):
    return redirect("events:next_event")


def next_event(request):
    events = models.Event.active_events()
    num_events = events.count()
    if num_events == 0:
        return redirect("events:last_events")
    if num_events == 1:
        event = events.first()
        return redirect("events:detail_event", slug=event.slug)
    return render(request, "events/list-events.html", {
        "title": "Próximos eventos",
        "breadcrumbs": breadcrumbs.bc_next_event(),
        "events": events.all(),
        })


def last_events(request):
    events = models.Event.active_events()[0:3]
    return render(request, "events/no-events.html", {
        "title": "Por el momento no hay eventos programados",
        "subtitle": "Estos son los 3 últimos eventos que hemos organizado.",
        "breadcrumbs": breadcrumbs.bc_last_events(),
        "events": events,
        })


def past_events(request):
    return render(request, "events/events-archive.html", {
        "titulo": "Archivo de eventos celebrados",
        "breadcrumbs": breadcrumbs.bc_past_events(),
        "events": models.Event.objects.filter(active=False),
        "archive": True,
        })


def detail_event(request, slug):
    event = models.Event.get_by_slug(slug)
    return render(request, "events/event.html", {
        "title": str(event),
        "breadcrumbs": breadcrumbs.bc_event(event),
        "event": event,
        })


def call_for_papers(request, event):
    initial = {}
    if request.method == "POST":
        form = forms.ProposalForm(event, request.POST)
        if form.is_valid():
            proposal = form.save()
            tasks.send_proposal_acknowledge.delay(proposal)
            tasks.send_proposal_notification.delay(proposal)
            return redirect(links.to_proposal_received(event))
    else:
        if request.user.is_authenticated:
            user = request.user
            initial['name'] = user.first_name
            initial['surname'] = user.last_name
            initial['email'] = user.email
        form = forms.ProposalForm(event, initial=initial)
    return render(request, "events/call-for-papers.html", {
        "title": f"Call for papers / {event}",
        "breadcrumbs": breadcrumbs.bc_event_cfp(event),
        "event": event,
        "form": form,
        })


def proposal_received(request, event):
    return render(request, "events/proposal_received.html", {
        "title": f"Gracias por su propuesta para {event}",
        "breadcrumbs": breadcrumbs.bc_proposal_received(event),
        "event": event,
        })


def waiting_list(request, event):
    if request.method == "POST":
        form = forms.WaitingListForm(event, request.POST)
        if form.is_valid():
            form.save()
            return redirect(links.to_waiting_list_accepted(event.slug))
    else:
        form = forms.WaitingListForm(event)
    return render(request, "events/waiting-list.html", {
        "title": f"Lista de espera para {event}",
        "breadcrumbs": breadcrumbs.bc_waiting_list(event),
        "event": event,
        "form": form,
        })


def waiting_list_accepted(request, event):
    return render(request, "events/waiting-list-accepted.html", {
        "title": "Su petición para la lista de espera está aceptada",
        "subtitle": str(event),
        "breadcrumbs": breadcrumbs.bc_waiting_list(event),
        "event": event,
        })


def refund(request, event):
    if request.method == "POST":
        form = forms.RefundForm(event, request.POST)
        if form.is_valid():
            ticket = form.ticket
            rf = models.Refund(ticket=ticket, event=event)
            rf.save()
            return redirect(links.to_refund_accepted(event, rf.pk))
    else:
        form = forms.RefundForm(event)
    return render(request, "events/refund.html", {
        "title": "Solicitud de devolución",
        "subtitle": str(event),
        "breadcrumbs": breadcrumbs.bc_refund(event),
        "event": event,
        "form": form,
        })


def refund_accepted(request, event, pk):
    refund = models.Refund.objects.get(pk=pk)
    return render(request, "events/refund-accepted.html", {
        "title": "Su solicitud de devolución de la entrada ha sido aceptada",
        "subtitle": str(event),
        "breadcrumbs": breadcrumbs.bc_refund_accepted(event, pk),
        "event": event,
        "refund": refund,
        })


# --------------------------------------------------------[ Sorteos ]--


def _warn_no_raffle(request, event):
    return render(request, "events/no-raffle.html", {
        "title": f"El evento {event} no tiene previsto sorteos",
        "breadcrumbs": breadcrumbs.bc_raffle(event),
        "event": event,
        })


@staff_member_required
def raffle(request, event):
    try:
        raffle = event.raffle
    except models.Event.raffle.RelatedObjectDoesNotExist:
        return _warn_no_raffle(request, event)
    gifts = raffle.gifts.all()
    candidate_tickets = raffle.get_candidate_tickets()
    num_tickets = candidate_tickets.count()
    if num_tickets > 0:
        success_probability = gifts.count() / candidate_tickets.count() * 100
    else:
        success_probability = None
    return render(request, "events/raffle.html", {
        "title": f"Sorteo {event}",
        "breadcrumbs": breadcrumbs.bc_raffle(event),
        "event": event,
        "gifts": gifts,
        "candidate_tickets": candidate_tickets,
        "success_probability": success_probability,
        })


@staff_member_required
def raffle_gifts(request, event):
    try:
        raffle = event.raffle
    except models.Event.raffle.RelatedObjectDoesNotExist:
        return _warn_no_raffle(request, event)
    gifts = raffle.gifts.all()
    return render(request, "events/raffle-gifts.html", {
        "title": f"Regalos previstos para el evento {event}",
        "breadcrumbs": breadcrumbs.bc_raffle_gifts(event),
        "event": event,
        "gifts": gifts,
        })


@staff_member_required
def raffle_gift(request, event, pk: int):
    try:
        raffle = event.raffle
    except models.Event.raffle.RelatedObjectDoesNotExist:
        return _warn_no_raffle(request, event)
    current_gift = Gift.objects.get(pk=pk)
    next_gift = raffle.get_undelivered_gifts().first()
    progress_value = current_gift.order() / raffle.gifts.count() * 100
    exist_available_tickets = raffle.get_available_tickets().count() > 0
    return render(request, "events/raffle-gift.html", {
        "title": f"Regalos {current_gift} para el evento {event}",
        "breadcrumbs": breadcrumbs.bc_raffle_gifts(event),
        "event": event,
        "current_gift": current_gift,
        "next_gift": next_gift,
        "progress_value": progress_value,
        "exist_available_tickets": exist_available_tickets,
        })



@staff_member_required
def raffle_gift_match(request, event, pk: int):
    try:
        raffle = event.raffle
    except models.Event.raffle.RelatedObjectDoesNotExist:
        return _warn_no_raffle(request, event)
    current_gift = Gift.objects.get(pk=pk)
    if current_gift.awarded_ticket:
        current_gift.missing_tickets.add(current_gift.awarded_ticket)
    current_gift.awarded_ticket = raffle.get_random_ticket()
    current_gift.awarded_at = DateTime.now()
    current_gift.save()
    return redirect(links.to_raffle(event))


@staff_member_required
def close_raffle(request, event):
    try:
        raffle = event.raffle
    except models.Event.raffle.RelatedObjectDoesNotExist:
        return _warn_no_raffle(request, event)
    if raffle.opened:
        raffle.closed_at = DateTime.now()
        raffle.save()
        messages.add_message(request, messages.SUCCESS, 'Sorteo cerrado')
    return redirect(links.to_raffle(event))


def raffle_results(request, event):
    try:
        raffle = event.raffle
    except models.Event.raffle.RelatedObjectDoesNotExist:
        return _warn_no_raffle(request, event)
    gifts = raffle.gifts.all()
    return render(request, "events/raffle-results.html", {
        "title": f"Resultados sorteo {event}",
        "breadcrumbs": breadcrumbs.bc_raffle_results(event),
        "event": event,
        "gifts": gifts,
        })


# --------------------------------------------------[ Pagos / Stripe ]--


def stripe_payment_declined(request, event, charge):
    return render(request, "events/payment-declined.html", {
        "title": "Error al realizar el cobro",
        "breadcrumbs": breadcrumbs.bc_payment_error(event),
        "charge_id": charge.id,
        })


def stripe_payment_error(request, event, exception):
    msg, extra_info = stripe_utils.get_description_from_exception(exception)
    return render(request, "events/payment-error.html", {
        "title": "Se ha producido un error al realizar el cobro",
        "breadcrumbs": breadcrumbs.bc_payment_error(event),
        "subtitle": msg,
        "extra_info": extra_info,
        "error": str(exception),
        })


def buy_ticket(request, event):
    if event.external_tickets_url:
        return redirect(event.external_tickets_url)
    all_articles = [a for a in event.all_articles()]
    active_articles = [a for a in all_articles if a.is_active()]
    num_active_articles = len(active_articles)
    if num_active_articles == 0:
        return no_available_articles(request, event, all_articles)
    elif num_active_articles == 1:
        article = active_articles[0]
        return redirect(links.to_ticket_purchase(article.pk))
    else:
        return select_article(request, event, all_articles, active_articles)


def no_available_articles(request, event, all_articles):
    organization = Organization.load_main_organization()
    return render(request, "events/no-available-articles.html", {
        "title": "No hay entradas disponibles",

        "subtitle": str(event),
        "event": event,
        "contact_email": organization.email,
        })


def select_article(request, event, all_articles, active_articles):
    return render(request, "events/select-article.html", {
        "title": "Seleccione el tipo de entrada",
        "breadcrumbs": breadcrumbs.bc_buy_ticket(event),
        "event": event,
        "all_articles": all_articles,
        "active_articles": active_articles,
        })


def ticket_purchase(request, id_article):
    article = Article.load_article(id_article)
    assert article.is_active(), "Este tipo de entrada no está ya disponible."
    event = article.event
    if request.method == "POST":
        form = forms.StripeForm(article, request.POST)
        if form.is_valid():
            result = form.charge_payment()
            if result.is_success():
                ticket = result.value['ticket']
                charge = result.value['charge']
                tasks.send_ticket.delay(ticket)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "El pago ha sido aprobado por Stripe",
                    )
                return redirect(links.to_article_bought(article.pk))
            else:
                msg = result.error_message
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"Error en el pago por stripe: {msg}",
                    )
                charge = result.extra.get('charge')
                return stripe_payment_declined(request, event, charge)
    else:
        form = forms.StripeForm(article)
    return render(request, "events/buy-article.html", {
        "title": "Compra de entradas",
        "subtitle": str(event),
        "breadcrumbs": breadcrumbs.bc_buy_ticket(event),
        "event": event,
        "article": article,
        'form': form,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        })


def ticket_purchase_nocc(request, id_article):
    article = Article.objects.select_related("event").get(pk=id_article)
    assert article.is_active(), "Este tipo de entrada no está ya disponible."

    template = "events/ticket-purchase-nocc.html"
    return render(request, template, {"article": article})


def article_bought(request, pk):
    article = Article.load_article(pk)
    assert article.is_active(), "Este tipo de entrada no está ya disponible."
    event = article.event
    return render(request, "events/article-bought.html", {
        "title": "Entrada comprada",
        "breadcrumbs": breadcrumbs.bc_article_bought(article),
        "article": article,
        "event": event,
        "contact_email": organization.email,
        })


def resend_ticket(request, event):
    form = forms.EmailForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            tickets = event.find_tickets_by_email(email)
            for ticket in tickets:
                tasks.send_ticket.delay(ticket)
            return redirect("events:resend_confirmation", slug=event.slug)
    return render(request, "events/resend-ticket.html", {
        "title": "Reenviar entrada",
        "subtitle": str(event),
        "breadcrumbs": breadcrumbs.bc_resend_ticket(event),
        "event": event,
        "form": form,
        })


def resend_confirmation(request, event):
    return render(request, "events/resend-confirmation.html", {
        "title": "Entrada reenviada",
        "subtitle": str(event),
        "breadcrumbs": breadcrumbs.bc_resend_confirmation(event),
        "event": event,
        })

