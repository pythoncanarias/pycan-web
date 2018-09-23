import logging
import io

import stripe
import pyqrcode

from libs.reports.core import Report

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

from tickets.models import Article
from tickets.models import Ticket
from events.models import Event
from events.tasks import send_ticket

from . import forms
from . import links
from . import stripe_utils

logger = logging.getLogger(__name__)


def index(request):
    events = Event.objects.filter(active=True)
    num_events = events.count()
    if num_events == 0:
        return render(request, 'events/no-events.html')
    if num_events == 1:
        event = events.first()
        return redirect('events:detail_event', slug=event.slug)
    else:
        return render(request, 'events/list_events.html', {
            'events': events.all()
            })


def detail_event(request, slug):
    event = Event.objects.get(slug=slug)
    return render(request, 'events/event.html', {
        'event': event,
    })


def stripe_payment_declined(request, charge):
    return render(request, 'events/payment_declined.html', {
        'email': settings.CONTACT_EMAIL,
        'charge_id': charge.id,
        }
    )


def stripe_payment_error(request, exception):
    msg, extra_info = stripe_utils.get_description_from_exception(exception)
    return render(request, 'events/payment_error.html', {
        'msg': msg,
        'extra_info': extra_info,
        'error': str(exception),
        'email': settings.CONTACT_EMAIL,
        }
    )


def buy_ticket(request, slug):
    logger.info("buy_tickts starts : slug={}".format(slug))
    event = Event.objects.get(slug=slug)
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
    return render(request, "events/no_available_articles.html", {
        'event': event,
        'contact_email': settings.CONTACT_EMAIL,
        })


def select_article(request, event, all_articles, active_articles):
    return render(request, "events/select_article.html", {
        'event': event,
        'all_articles': all_articles,
        'active_articles': active_articles,
        })



def ticket_purchase(request, id_article):
    article = Article.objects.select_related('event').get(pk=id_article)
    assert article.is_active(), "Este tipo de entrada no está ya disponible."
    event = article.event
    if request.method == 'POST':
        email = request.POST['stripeEmail']
        name = request.POST['name']
        surname = request.POST['surname']
        phone = request.POST.get('phone', None)
        token = request.POST['stripeToken']
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            customer = stripe.Customer.create(
                email=email,
                source=token,
                description='{}, {}'.format(surname, name),
            )
            charge = stripe.Charge.create(
                customer=customer.id,
                amount=article.price_in_cents,
                currency='EUR',
                description='{} for {}, {}'.format(
                    article.category.name,
                    surname,
                    name,
                )
            )
            if charge.paid:
                ticket = Ticket(
                    article=article,
                    number=article.next_number(),
                    customer_name=name,
                    customer_surname=surname,
                    customer_email=email,
                    customer_phone=phone,
                    payment_id=charge.id,
                    )
                ticket.save()
                send_ticket.delay(ticket)
                return redirect(ticket.get_absolute_url())
            else:
                return stripe_payment_declined(request, charge)
        except stripe.error.StripeError as err:
            logger.error('Error de stripe')
            logger.error(str(err))
            return stripe_payment_error(request, err)
        except Exception as err:
            logger.error('Error en el pago por stripe')
            logger.error(str(err))
            messages.add_message(request, messages.ERROR, 'Hello world.')
            from django.http import HttpResponse
            return HttpResponse("Something goes wrong\n{}".format(err))
    else:
        return render(request, 'events/buy_article.html', {
            'event': event,
            'article': article,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            })


def ticket_bought(request, keycode):
    ticket = Ticket.objects.get(keycode=keycode)
    article = ticket.article
    event = article.event
    return render(request, 'events/ticket_bought.html', {
        'ticket': ticket,
        'article': article,
        'event': event,
        })


def ticket_qrcode(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    img = pyqrcode.create(str(ticket.keycode))
    buff = io.BytesIO()
    img.svg(buff, scale=8)
    return HttpResponse(
        buff.getvalue(),
        content_type='image/svg+xml',
        )


def coc(request, language='es'):
    template = 'events/coc_{}.html'.format(language)
    return render(request, template)


def find_tickets_by_email(event, email):
    qs = event.all_tickets().filter(customer_email=email)
    return list(qs)


def resend_ticket(request, slug):
    event = Event.objects.get(slug=slug)
    form = forms.EmailForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            tickets = find_tickets_by_email(event, email)
            for ticket in tickets:
                send_ticket.delay(ticket)
            return redirect('events:resend_confirmation', slug=event.slug)
    return render(request, 'events/resend_ticket.html', {
        'event': event,
        'form': form,
    })


def resend_confirmation(request, slug):
    event = Event.objects.get(slug=slug)
    return render(request, 'events/resend_confirmation.html', {
        'event': event,
        'contact_email': settings.CONTACT_EMAIL,
        })
