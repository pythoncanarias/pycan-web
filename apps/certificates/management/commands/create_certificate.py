#!/usr/bin/env python

from django.core.management.base import BaseCommand

from certificates.utils import create_certificate
from tickets.models import Ticket


class Command(BaseCommand):
    help = "Generate certificates"

    def add_arguments(self, parser):
        parser.add_argument('ticket_id', type=int, action='store')
        parser.add_argument(
            '--trace-off',
            dest='tron',
            default=True,
            action='store_false',
            help='No output in success, only objects in case of errors'
            )

    def handle(self, *args, **options):
        tron = options.get('tron', True)
        ticket_id = options['ticket_id']
        ticket = Ticket.objects.get(pk=ticket_id)
        if tron:
            print('Creating certificate for ticket {}'.format(ticket))
        output_filename = create_certificate(
            'attendance',
            output_name=ticket.keycode,
            name=ticket.customer_full_name,
            )
        if tron:
            print('File {} created'.format(output_filename))
