#!/usr/bin/env python3

from django.core.management.base import BaseCommand

from rich.console import Console
from rich.table import Table

from apps.events.models import Event


def red(txt):
    return f'[red]{txt}[/red]'


def green(txt):
    return f'[green]{txt}[/green]'


def cyan(txt):
    return f'[cyan]{txt}[/cyan]'


class Command(BaseCommand):

    help = 'Gestión de eventos'

    def __init__(self, *args, **kwargs):
        self.console = Console()
        super().__init__(*args, **kwargs)

    def print(self, *args, **kwargs):
        self.console.print(*args, **kwargs)

    def add_arguments(self, parser):
        self.parser = parser
        parser.add_argument('--verbose', action='store_true', help='Verbose mode')
        subparser = parser.add_subparsers(dest="subcommand")
        list_parser = subparser.add_parser("list")
        list_parser.add_argument(
            '-a',
            '--all',
            type=bool,
            default=False,
            help="Listar todos los eventos",
        )
        list_parser.add_argument(
            '-n',
            '--num',
            type=int,
            default=25,
            help="Numero de eventos a mostrar (Primero los más recientes)",
        )

    def do_list(self, *args, **options):
        events = Event.objects.all()
        num = options.get('num')
        list_all = options.get('all')
        if list_all:
            title = "Listado de todos los eventos"
        else:
            events = events[0:num]
            title = f"listado de los últimos {num} eventos"
        tab = Table(title=title)
        tab.add_column("Id", justify="right")
        tab.add_column("Tag", justify="right")
        tab.add_column("Nombre")
        for event in events:
            tab.add_row(
                str(event.pk),
                event.hashtag,
                event.name,
                )
        self.print(tab)

    def handle(self, *args, **options):
        subcommand = options.get('subcommand') or 'list'
        self.print(subcommand)
        do_cmd = getattr(self, f'do_{subcommand}', None)
        if callable(do_cmd):
            do_cmd(*args, **options)
