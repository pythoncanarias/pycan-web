#!/usr/bin/env python


from django.core.management.base import BaseCommand
from certificates.utils import create_certificate
from tickets.models import Ticket


class Command(BaseCommand):
    help = "Generate certificates"

    def add_arguments(self, parser):
        parser.add_argument('ticket_id', type=int, action='store')

    def handle(self, *args, **options):
        ticket_id = options['ticket_id']
        ticket = Ticket.objects.get(pk=ticket_id)
        create_certificate(
            'attendance',
            output_name=ticket.keycode,
            name=ticket.customer_full_name,
            )

