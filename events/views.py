from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import stripe
from tickets.models import Ticket
from events.models import Event
from events.tasks import send_ticket

from . import forms
from libs.reports.core import Report
import pyqrcode
import io
from . import stripe_utils


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
    event = Event.objects.get(slug=slug)
    all_articles = [a for a in event.all_articles()]
    active_articles = [a for a in all_articles if a.is_active()]
    num_active_articles = len(active_articles)
    # num_active_articles = 1
    if num_active_articles == 0:
        return no_available_articles(request, event, all_articles)
    elif num_active_articles == 1:
        article = active_articles[0]
        return buy_article(request, event, article)
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


def buy_article(request, event, article):
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
                    article.name,
                    surname,
                    name,
                )
            )
            if charge.paid:
                ticket = Ticket(
                    article=article,
                    number=article.next_number(),
                    name=name,
                    surname=surname,
                    email=email,
                    phone=phone,
                    )
                ticket.save()
                return redirect(ticket.get_absolute_url())
            else:
                return stripe_payment_declined(request, charge)
        except stripe.error.StripeError as err:
            return stripe_payment_error(request, err)
    else:
        return render(request, 'events/buy_ticket.html', {
            'event': event,
            'article': article,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            })


def ticket_bought(request, keycode):
    ticket = Ticket.objects.get(keycode=keycode)
    ticket_type = ticket.ticket_type
    event = ticket_type.event
    return render(request, 'events/ticket_bought.html', {
        'ticket': ticket,
        'ticket_type': ticket_type,
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


def ticket_pdf(request, keycode):
    ticket = Ticket.objects.get(keycode=keycode)
    return Report(
        'events/ticket.j2',
        {
            'ticket': ticket,
            'qrcode_url': request.build_absolute_uri(ticket.get_qrcode_url())
        },
    ).render()


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
