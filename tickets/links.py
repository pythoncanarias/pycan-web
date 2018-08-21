from django.urls import reverse


def index():
    '''Returns link to events entry point.
    '''
    return reverse('events:index')


def qr_code(id_ticket):
    '''Returns link to the qr_code image of a ticket.
    '''
    return reverse('events:ticket_qrcode', kwargs={'pk': id_ticket})
