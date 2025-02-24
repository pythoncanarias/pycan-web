from inspect import getmembers, isfunction

from django.core.management.base import BaseCommand
from rich.console import Console
from rich.table import Table

from apps.notices import repository
from apps.notices.models import Notice, NoticeKind
from apps.notices.tasks import (
    create_notice_body,
    create_notice_message,
    task_send_notice,
)


NOTICE_KIND = dict(getmembers(repository, isfunction))


def red(txt):
    return f'[red]{txt}[/red]'


def green(txt):
    return f'[green]{txt}[/green]'


def cyan(txt):
    return f'[cyan]{txt}[/cyan]'


def yes_no(flag, yes='Si', no='no'):
    return green(yes) if flag else red(no)


class Command(BaseCommand):

    help = 'Gestión de avisos a socios'

    def __init__(self, *args, **kwargs):
        self.console = Console()
        super().__init__(*args, **kwargs)

    def print(self, *args, **kwargs):
        self.console.print(*args, **kwargs)

    def add_arguments(self, parser):
        self.parser = parser
        parser.add_argument('--verbose', action='store_true', help='Verbose mode')
        subparser = parser.add_subparsers(dest="subcommand")
        # run
        run_parser = subparser.add_parser("run")
        run_parser.add_argument('--check', action='store_true')
        # message
        message_parser = subparser.add_parser("message")
        message_parser.add_argument("id_notice", type=int)
        # list
        list_parser = subparser.add_parser("list")
        list_parser.add_argument(
            '-n',
            '--num_rows',
            type=int,
            default=25,
            help="Numero de resultados a mostrar",
        )
        # rules
        rules_parser = subparser.add_parser("rules")
        rules_parser.add_argument(
            '--enable',
            type=int,
            help="Activar un tipo de aviso",
        )
        rules_parser.add_argument(
            '--disable',
            type=int,
            help="Desactivar un tipo de aviso",
        )

    def do_message(self, *args, **options):
        id_notice = options.get('id_notice')
        notice = Notice.load_notice(id_notice)
        email_message = create_notice_message(notice)
        self.print(
            cyan('From:'),
            f'{email_message._from_email._email}'
            f' <{email_message._from_email._name}>',
        )
        self.print(cyan('Subject:'), email_message._subject)
        self.print()
        self.print(create_notice_body(notice))
        self.print()

    def print_table_notices(self, notices):
        tab = Table(title="Last notices (last {num_rows})")
        tab.add_column("Id. msg", justify="right")
        tab.add_column("Member")
        tab.add_column("Notice")
        tab.add_column("Ref. date")
        tab.add_column("Delivered")
        for notice in notices:
            tab.add_row(
                str(notice.pk),
                str(notice.member),
                str(notice.kind),
                str(notice.reference_date),
                yes_no(notice.status()),
                )
        self.print(tab)

    def do_list(self, *args, **options):
        num_rows = options.get('num_rows')
        notices = list(Notice.objects.order_by('-created_at')[0:num_rows])
        if notices:
            self.print_table_notices(notices)
        else:
            self.print(cyan('No hay ningún aviso en la base de datos'))

    def print_table_rules(self, rules):
        tab = Table(title="Rules")
        tab.add_column("Id. rule", justify="right")
        tab.add_column("Description")
        tab.add_column("Code")
        tab.add_column("Days")
        tab.add_column("Enabled")
        for rule in rules:
            status_code = callable(NOTICE_KIND.get(rule.code))
            tab.add_row(
                str(rule.pk),
                rule.description,
                green(rule.code) if status_code else red(rule.code),
                str(rule.days),
                yes_no(rule.enabled),
                )
        self.print(tab)

    def do_rules(self, *args, **options):
        body = []
        id_to_enable = options.get('enable')
        id_to_disable = options.get('disable')
        if id_to_enable and id_to_disable and id_to_enable == id_to_disable:
            self.print(red("Las dos opciones son mutuamente exclueyentes"))
            return
        if id_to_enable:
            kind = NoticeKind.objects.get(pk=id_to_enable)
            if not kind.enabled:
                kind.enabled = True
                kind.save()
        if id_to_disable:
            kind = NoticeKind.objects.get(pk=id_to_disable)
            if kind.enabled:
                kind.enabled = False
                kind.save()
        self.print_table_rules(NoticeKind.objects.all().order_by('pk'))

    def print_table_checks(self, cheks):
        tab = Table(title="Checks run")
        tab.add_column("Member")
        tab.add_column("Notice")
        tab.add_column("Ref. date")
        tab.add_column("Status")
        for check in checks:
            tab.add_row(*check)
        self.print(tab)

    def do_run(self, **options):
        is_verbose = options.get('verbose')
        is_check = options.get('check')
        body = []
        for kind in NoticeKind.objects.filter(enabled=True).all():
            code = NOTICE_KIND.get(kind.code)
            if not code:
                self.print(red(f"ERROR: No existe {kind.code}"))
                continue
            if callable(code):
                for ref_date, member in code(days=kind.days):
                    notice = kind.notice_has_been_send(member, ref_date)
                    if notice:
                        status = green("[Skipped]")
                    else:
                        if is_check:
                            status = green("[Notice would be queued]")
                        else:
                            notice = kind.send_notice(member, ref_date)
                            task_send_notice.delay(notice)
                            status = cyan("[Notice queued]")
                    body.append((member, notice.kind, ref_date, status))
        if body and (is_verbose or is_check):
            self.print_table_checks(body)

    def handle(self, *args, **options):
        subcommand = options.get('subcommand')
        if subcommand:
            do_cmd = getattr(self, f'do_{subcommand}', None)
            if callable(do_cmd):
                do_cmd(*args, **options)
        else:
            self.parser.print_help()
