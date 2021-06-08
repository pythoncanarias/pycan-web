import decimal
import logging
import datetime

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max

from utils.console import green, red, cyan, as_table, yes_no
from apps.notices.models import Notice, NoticeKind
from apps.members.models import Member
from apps.notices.tasks import (
    task_send_notice,
    create_notice_message,
    create_notice_body,
)

logger = logging.getLogger(__name__)


def autotest(days=0):
    logger.info("autotest starts")
    DEVELOPERS = ['sdelquin', 'euribates']  # ToDo: Put this info in database
    hoy = timezone.now().date()
    for username in DEVELOPERS:
        member = Member.load_from_username(username)
        yield hoy, member


def members_nearly_expired(days=0):
    logger.info("members_nearly_expired starts")
    hoy = timezone.now().date()
    if days <= 0:
        from_date = hoy
        to_date = hoy + datetime.timedelta(days=-days+1)
    else:
        from_date = hoy + datetime.timedelta(days=days)
        to_date = from_date + datetime.timedelta(days=12)
    qs = (
        Member.objects
        .annotate(max_valid_until=Max('membership__valid_until'))
        .filter(max_valid_until__isnull=False)
        .filter(max_valid_until__gte=from_date)
        .filter(max_valid_until__lt=to_date)
    )
    for m in qs:
        yield m.max_valid_until, m


class Command(BaseCommand):

    help = 'Gestión de avisos a socios'

    def add_arguments(self, parser):
        self.parser = parser
        parser.add_argument('--verbose', action='store_true', help='Verboso')
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
            '-n', '--num_rows',
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
        notice = Notice.objects.get(pk=id_notice)
        email_message = create_notice_message(notice)
        print(
            cyan('From:'),
            f'{email_message._from_email._email}'
            f' <{email_message._from_email._name}>',
        )
        print(cyan('Subject:'), email_message._subject)
        print()
        print(create_notice_body(notice))
        print()

    def do_list(self, *args, **options):
        num_rows = options.get('num_rows')
        body = list(
            (
                notice.pk,
                notice.member,
                notice.kind,
                notice.reference_date,
                yes_no(notice.status()),
            )
            for notice in Notice
                .objects
                .order_by('-created_at')
                [0:num_rows]
        )
        if body:
            headers = ['Msg.', 'Member', 'Notice', 'Ref. date', 'delivered']
            print(as_table(headers, body))
        else:
            print(cyan('No hay ningún aviso en la base de datos'))

    def do_rules(self, *args, **options):
        body = []
        id_to_enable = options.get('enable')
        id_to_disable = options.get('disable')
        if id_to_enable and id_to_disable and id_to_enable == id_to_disable:
            print(red("Las dos opciones son mutuamente exclueyentes"))
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
        for kind in NoticeKind.objects.all().order_by('pk'):
            status_code = callable(globals().get(kind.code))
            body.append((
                kind.pk,
                kind.description,
                green(kind.code) if status_code else red(kind.code),
                kind.days,
                yes_no(kind.enabled),
            ))
        headers = ["Id.", "Description", "Code", "Days", "Enabled"]
        print(as_table(headers, body))

    def do_run(self, **options):
        is_verbose = options.get('verbose')
        is_check = options.get('check')
        body = []
        for kind in NoticeKind.objects.filter(enabled=True).all():
            code = globals().get(kind.code)
            if not code:
                print(red(f"ERROR: No existe {kind.code}"))
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
        if is_verbose or is_check:
            headers = ['Member', 'Notice', 'Ref. date', 'Status']
            print(as_table(headers, body))

    def handle(self, *args, **options):
        subcommand = options.get('subcommand')
        if subcommand:
            do_cmd = getattr(self, f'do_{subcommand}', None)
            if callable(do_cmd):
                do_cmd(*args, **options)
        else:
            self.parser.print_help()
