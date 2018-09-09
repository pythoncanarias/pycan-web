from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import stripe
from . import models
from libs.reports.core import Report
import pyqrcode
import io
from . import stripe_utils


def index(request):
    events = models.Event.objects.filter(active=True)
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
    event = models.Event.objects.get(slug=slug)
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


def buy_ticket(request, id_ticket_type):
    ticket_type = models.TicketType.objects  \
        .select_related('event')  \
        .get(pk=id_ticket_type)
    event = ticket_type.event
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
                amount=ticket_type.price_in_cents,
                currency='EUR',
                description='{} for {}, {}'.format(
                    ticket_type.name,
                    surname,
                    name,
                )
            )
            if charge.paid:
                ticket = models.Ticket(
                    ticket_type=ticket_type,
                    number=ticket_type.next_number(),
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
            'ticket_type': ticket_type,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            })


def ticket_bought(request, keycode):
    ticket = models.Ticket.objects.get(keycode=keycode)
    ticket_type = ticket.ticket_type
    event = ticket_type.event
    return render(request, 'events/ticket_bought.html', {
        'ticket': ticket,
        'ticket_type': ticket_type,
        'event': event,
        })


def ticket_qrcode(request, pk):
    ticket = models.Ticket.objects.get(pk=pk)
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
    ticket = models.Ticket.objects.get(keycode=keycode)
    return Report(
        'events/ticket.j2',
        {
            'ticket': ticket,
            'qrcode_url': request.build_absolute_uri(ticket.get_qrcode_url())
        },
    ).render()
