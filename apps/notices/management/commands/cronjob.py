from django.core.management.base import BaseCommand, CommandError

from apps.members.models import Member

class Command(BaseCommand):

    help = 'Gestión de avisos a socios'

    def add_arguments(self, parser):
        parser.add_argument('--verbose', action='store_true', help='Verboso')
        subparser = parser.add_subparsers(dest="subcommand")
        before7d_parser = subparser.add_parser("before7d")
        before7d_parser.add_argument('--check', action='store_true')

    def do_before7d(self, *args, **options):
        is_check = options.get('check')
        print('ok')
        print(f'is check is {is_check}')
        for miembro in Miembro.objects.all():
            print(miembro)


    def handle(self, *args, **options):
        subcommand = options.get('subcommand')
        print('subcommand is', subcommand)
        do_callable = getattr(self, f'do_{subcommand}')
        do_callable(*args, **options)
