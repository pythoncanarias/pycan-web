from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import stripe
from . import models
from libs.reports.core import Report
import pyqrcode
import io


def index(request):
    events = models.Event.objects.filter(active=True)
    num_events = events.count()
    if num_events == 0:
        return render(request, 'events/no-events.html')
    if num_events == 1:
        event = events.first()
        return _view_event(request, event)
    else:
        return render(request, 'events/list-events.html', {
            'events': events.all()
            })


def detail_event(request, slug):
    event = models.Event.objects.get(slug=slug)
    return _view_event(request, event)


def _view_event(request, event):
    ticket_types = event.ticket_types.all().order_by('release_at')
    num_options = ticket_types.count()
    return render(request, 'events/event.html', {
        'event': event,
        'ticket_types': ticket_types,
        'num_options': num_options,
        })


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
            # Must implemente a proper response
            return HttpResponse(
                'Nope. Algo fallo en el pago: charge:{}'.format(charge)
                )
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


def coc(request, language):
    if language:
        template = f'coc_{language}.html'
    else:
        template = f'coc.html'
    template_path = 'events/' + template
    return render(request, template_path)


def ticket_pdf(request, keycode):
    ticket = models.Ticket.objects.get(keycode=keycode)
    return Report(
        'events/ticket.j2',
        {
            'ticket': ticket,
            'qrcode_url': request.build_absolute_uri(ticket.get_qrcode_url())
        },
    ).render()
