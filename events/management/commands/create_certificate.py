#!/usr/bin/env python

import os
import re
import subprocess

from django.core.management.base import BaseCommand

import events
from tickets.models import Ticket


def get_full_name(filename, base=os.path.dirname(events.__file__)):
    return os.path.join(base, 'certificates', filename)


def inkscape_export(source_filename, target_filename):
    commands = ["inkscape", "--export-pdf={}".format(target_filename), source_filename]
    print(" ".join(commands))
    subprocess.call(commands)


def create_certificate(template, ticket):
    pat = re.compile(r'(\{\{.+\}\})')
    name = '{} {}'.format(ticket.customer_name, ticket.customer_surname)
    full_input_name = get_full_name('{}.svg'.format(template))
    full_output_name = get_full_name('{}.svg'.format(ticket.keycode))
    with open(full_input_name, 'r') as fin:
        with open(full_output_name, 'w') as fout:
            template = fin.read()
            output = pat.sub(name, template)
            fout.write(output)
    pdf_filename = get_full_name('{}.pdf'.format(ticket.keycode))
    inkscape_export(full_output_name, pdf_filename)


class Command(BaseCommand):
    help = "Generate certificates"

    def add_arguments(self, parser):
        parser.add_argument('ticket_id', type=int, action='store')

    def handle(self, *args, **options):
        ticket_id = options['ticket_id']
        ticket = Ticket.objects.get(pk=ticket_id)
        create_certificate('attendance', ticket)
