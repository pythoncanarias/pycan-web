import datetime
import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.urls import reverse
from apps.organizations.models import Organization
from apps.tickets.models import Article, Gift, Raffle, Ticket

from . import forms, links, stripe_utils
from .models import Event, Refund, WaitingList
from .tasks import send_ticket
from .forms import ProposalForm

logger = logging.getLogger(__name__)


def index(request):
    return redirect("events:next")


def next(request):
    events = Event.objects.filter(active=True).order_by("-start_date")
    num_events = events.count()
    if num_events == 0:
        past_events = Event.objects.all().order_by("-start_date")[0:3]
        return render(
            request,
            "events/no-events.html",
            {
                "past_events": past_events,
            },
        )
    if num_events == 1:
        event = events.first()
        return redirect("events:detail_event", slug=event.slug)
    else:
        return render(request, "events/list-events.html", {"events": events.all()})


def detail_event(request, slug):
    event = Event.get_by_slug(slug)
    past_events = (
        Event.objects.filter(active=False)
        .exclude(pk=event.id)
        .order_by("-start_date")[:3]
    )
    return render(
        request,
        "events/event.html",
        {"event": event, "past_events": past_events},
    )


def call_for_papers(request, event):
    if request.method == "POST":
        form = ProposalForm(event, request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("events:thanks"))
    else:
        form = ProposalForm(event)
    return render(
        request,
        "events/call-for-papers.html",
        {
            "tille": f"Call for papers / {event}",
            "event": event,
            "form": form,
        },
    )


def proposal_received(request):
    from django.http import HttpResponse

    return HttpResponse(" no implementado", content_type="text/plain")


def waiting_list(request, slug):
    event = Event.get_by_slug(slug)
    if request.method == "POST":
        form = forms.WaitingListForm(request.POST)
        if form.is_valid():
            wl = WaitingList(
                event=event,
                name=form.cleaned_data["name"],
                surname=form.cleaned_data["surname"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
            )
            wl.save()
            return redirect(links.waiting_list_accepted(event.slug))
    else:
        form = forms.WaitingListForm()
    return render(
        request,
        "events/waiting-list.html",
        {
            "event": event,
            "form": form,
        },
    )


def refund(request, slug):
    logging.error('refund(request, "{}") starts'.format(slug))
    event = Event.get_by_slug(slug)
    logging.error("   request method is {}".format(request.method))
    if request.method == "POST":
        form = forms.RefundForm(event, request.POST)
        logging.error("   form.is_valid() is {}".format(form.is_valid()))
        logging.error("   form.errors is {}".format(form.errors))
        if form.is_valid():
            ticket = form.ticket
            rf = Refund(ticket=ticket, event=event)
            rf.save()
            return redirect(links.refund_accepted(event.slug, rf.pk))
    else:
        form = forms.RefundForm(event)
    return render(
        request,
        "events/refund.html",
        {
            "event": event,
            "form": form,
        },
    )


def refund_accepted(request, slug, pk):
    event = Event.get_by_slug(slug)
    refund = Refund.objects.get(pk=pk)
    return render(
        request,
        "events/refund-accepted.html",
        {
            "event": event,
            "refund": refund,
        },
    )


def waiting_list_accepted(request, slug):
    event = Event.get_by_slug(slug)
    return render(
        request,
        "events/waiting-list-accepted.html",
        {
            "event": event,
        },
    )


def trade(request, slug, sell_code, buy_code):
    event = Event.get_by_slug(slug)
    refund = Refund.load_by_sell_code(sell_code)
    waiting_list = WaitingList.load_by_buy_code(buy_code)
    """Pseudo codigo
    GET:
    1) A partir del ticket comprado obtener el tipo de ticket (articulo)
    2) A partir del waiting list, obtener los datos del nuevo comprador
    3) Preparar el formulario de compra. Idealmente un solo boton
    POST:
    1) obtener timestamp
    2) Marcar el waiting list como fixed
    3) Marcar el refund como fixed
    4) Notificar a ambos que el acuerdo esta cerrado
    """

    return render(
        request,
        "events/trade.html",
        {
            "event": event,
            "waiting_list": waiting_list,
            "refund": refund,
        },
    )


def stripe_payment_declined(request, charge):
    organization = Organization.load_main_organization()
    return render(
        request,
        "events/payment-declined.html",
        {
            "email": organization.email,
            "charge_id": charge.id,
        },
    )


def stripe_payment_error(request, exception):
    msg, extra_info = stripe_utils.get_description_from_exception(exception)
    organization = Organization.load_main_organization()
    return render(
        request,
        "events/payment-error.html",
        {
            "msg": msg,
            "extra_info": extra_info,
            "error": str(exception),
            "email": organization.email,
        },
    )


def buy_ticket(request, slug):
    logger.debug("buy_tickts starts : slug={}".format(slug))
    event = Event.get_by_slug(slug)
    if event.external_tickets_url:
        logger.debug(
            "Redirecting to external URL for selling tickets: url={}".format(
                event.external_tickets_url
            )
        )
        return redirect(event.external_tickets_url)
    all_articles = [a for a in event.all_articles()]
    active_articles = [a for a in all_articles if a.is_active()]
    num_active_articles = len(active_articles)
    # num_active_articles = 1
    if num_active_articles == 0:
        return no_available_articles(request, event, all_articles)
    elif num_active_articles == 1:
        article = active_articles[0]
        return redirect(links.ticket_purchase(article.pk))
    else:
        return select_article(request, event, all_articles, active_articles)


def no_available_articles(request, event, all_articles):
    organization = Organization.load_main_organization()
    return render(
        request,
        "events/no-available-articles.html",
        {
            "event": event,
            "contact_email": organization.email,
        },
    )


def select_article(request, event, all_articles, active_articles):
    return render(
        request,
        "events/select-article.html",
        {
            "event": event,
            "all_articles": all_articles,
            "active_articles": active_articles,
        },
    )


def ticket_purchase(request, id_article):
    article = Article.objects.select_related("event").get(pk=id_article)
    assert article.is_active(), "Este tipo de entrada no está ya disponible."
    event = article.event
    if request.method == "POST":
        email = request.POST["stripeEmail"]
        name = request.POST["name"]
        surname = request.POST["surname"]
        phone = request.POST.get("phone", None)
        token = request.POST["stripeToken"]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            customer = stripe.Customer.create(
                email=email,
                source=token,
                description="{}, {}".format(surname, name),
            )
            charge = stripe.Charge.create(
                customer=customer.id,
                amount=article.price_in_cents,
                currency="EUR",
                description="{}/{}, {}".format(
                    event.hashtag,
                    surname,
                    name,
                ),
            )
            if charge.paid:
                ticket = Ticket(
                    article=article,
                    customer_name=name,
                    customer_surname=surname,
                    customer_email=email,
                    customer_phone=phone,
                    payment_id=charge.id,
                )
                ticket.save()
                send_ticket.delay(ticket)
                return redirect(links.article_bought(article.pk))
            else:
                return stripe_payment_declined(request, charge)
        except stripe.error.StripeError as err:
            logger.error("Error de stripe")
            logger.error(str(err))
            return stripe_payment_error(request, err)
        except Exception as err:
            logger.error("Error en el pago por stripe")
            logger.error(str(err))
            messages.add_message(request, messages.ERROR, "Hello world.")
            from django.http import HttpResponse

            return HttpResponse("Something goes wrong\n{}".format(err))
    else:
        return render(
            request,
            "events/buy-article.html",
            {
                "event": event,
                "article": article,
                "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            },
        )


def ticket_purchase_nocc(request, id_article):
    article = Article.objects.select_related("event").get(pk=id_article)
    assert article.is_active(), "Este tipo de entrada no está ya disponible."

    template = "events/ticket-purchase-nocc.html"
    return render(request, template, {"article": article})


def article_bought(request, id_article):
    article = Article.objects.select_related("event").get(pk=id_article)
    assert article.is_active(), "Este tipo de entrada no está ya disponible."
    event = article.event
    organization = Organization.load_main_organization()
    return render(
        request,
        "events/article-bought.html",
        {
            "article": article,
            "event": event,
            "contact_email": organization.email,
        },
    )


def find_tickets_by_email(event, email):
    qs = event.all_tickets().filter(customer_email=email)
    return list(qs)


def resend_ticket(request, slug):
    event = Event.get_by_slug(slug)
    form = forms.EmailForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            tickets = find_tickets_by_email(event, email)
            for ticket in tickets:
                send_ticket.delay(ticket)
            return redirect("events:resend_confirmation", slug=event.slug)
    return render(
        request,
        "events/resend-ticket.html",
        {
            "event": event,
            "form": form,
        },
    )


def resend_confirmation(request, slug):
    event = Event.get_by_slug(slug)
    organization = Organization.load_main_organization()
    return render(
        request,
        "events/resend-confirmation.html",
        {
            "event": event,
            "contact_email": organization.email,
        },
    )


def past_events(request):
    events = Event.objects.filter(active=False).order_by("-start_date")
    return render(
        request,
        "events/list-events.html",
        {"events": events.all(), "archive": True},
    )


@staff_member_required
def raffle(request, slug):
    try:
        event = Event.get_by_slug(slug)
        raffle = event.raffle
    except (Event.DoesNotExist, Raffle.DoesNotExist):
        return redirect("/")
    gifts = raffle.gifts.all()
    candidate_tickets = raffle.get_candidate_tickets()
    success_probability = gifts.count() / candidate_tickets.count() * 100
    return render(
        request,
        "events/raffle.html",
        {
            "event": event,
            "raffle": raffle,
            "gifts": gifts,
            "candidate_tickets": candidate_tickets,
            "success_probability": success_probability,
        },
    )


@staff_member_required
def raffle_gift(request, slug, gift_id, match=False):
    try:
        event = Event.get_by_slug(slug)
        raffle = event.raffle
    except (Event.DoesNotExist, Raffle.DoesNotExist):
        return redirect("/")
    current_gift = Gift.objects.get(pk=gift_id)
    if match:
        if current_gift.awarded_ticket:
            current_gift.missing_tickets.add(current_gift.awarded_ticket)
        current_gift.awarded_ticket = raffle.get_random_ticket()
        current_gift.awarded_at = datetime.datetime.now()
        current_gift.save()
    next_gift = raffle.get_undelivered_gifts().first()
    progress_value = current_gift.order() / raffle.gifts.count() * 100
    exist_available_tickets = raffle.get_available_tickets().count() > 0
    return render(
        request,
        "events/raffle-gift.html",
        {
            "event": event,
            "current_gift": current_gift,
            "next_gift": next_gift,
            "match": match,
            "progress_value": progress_value,
            "exist_available_tickets": exist_available_tickets,
        },
    )


def raffle_results(request, slug):
    try:
        event = Event.get_by_slug(slug)
        raffle = event.raffle
    except (Event.DoesNotExist, Raffle.DoesNotExist):
        return redirect("/")
    if request.user.is_staff and raffle.opened:
        raffle.closed_at = datetime.datetime.now()
        raffle.save()
    gifts = raffle.gifts.all()
    return render(
        request, "events/raffle-results.html", {"event": event, "gifts": gifts}
    )
