import decimal
import datetime

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max

from apps.notices.models import Notice, NoticeKind
from apps.members.models import Member
from apps.notices.tasks import (
    task_send_notice,
    create_notice_message,
    create_notice_body,
)



def red(s):
    return f"\u001b[31m{s}\u001b[0m"


def cyan(s):
    return f"\u001b[36m{s}\u001b[0m"


def green(s):
    return f"\u001b[32m{s}\u001b[0m"


def as_cell(val, width):
    if isinstance(val, (int, float, decimal.Decimal, bool)):
        return f"{{:>{width}}}".format(str(val))
    else:
        return f"{{:<{width}}}".format(str(val))


def as_table(headers, rows):
    assert all([
        len(headers) == len(row)
        for row in rows
        ])
    result = []
    widths = [len(str(head)) for head in headers]
    for row in rows:
        widths = [
            max(a, len(str(b)))
            for a, b in zip(widths, row)
        ]
    result.append(' '.join([as_cell(h, w) for h, w in zip(headers, widths)]))
    result.append(' '.join(['-' * w for w in widths]))
    for row in rows:
        result.append(' '.join([as_cell(v, w) for v, w in zip(row, widths)]))
    result.append(' '.join(['-' * w for w in widths]))
    return '\n'.join(result)



def members_nearly_expired(days=0):
    days = days + 1
    qs = (
        Member.objects
        .filter(membership__valid_until__isnull=False)
        .annotate(valid_until=Max('membership__valid_until'))
    )
    hoy = datetime.date.today()
    last_day = hoy + datetime.timedelta(days=days)
    return [
        m for m in qs
        if m.valid_until >= hoy and m.valid_until < last_day
    ]



class Command(BaseCommand):

    help = 'Gestión de avisos a socios'

    def add_arguments(self, parser):
        parser.add_argument('--verbose', action='store_true', help='Verboso')
        subparser = parser.add_subparsers(dest="subcommand")
        before7d_parser = subparser.add_parser("before7d")
        before7d_parser.add_argument('--check', action='store_true')
        run_parser = subparser.add_parser("run")
        list_parser = subparser.add_parser("list")
        message_parser = subparser.add_parser("message")
        message_parser.add_argument("id_notice", type=int)

    def do_message(self, *args, **options):
        id_notice = options.get('id_notice')
        notice = Notice.objects.get(pk=id_notice)
        email_message = create_notice_message(notice)
        print('From:', f'{email_message._from_email._email} <{email_message._from_email._name}>')
        print('Subject:', email_message._subject)
        print()
        print(create_notice_body(notice))

    def do_list(self, *args, **kwargs):
        headers = ['pk', 'code', 'member', 'ref. date', 'status']
        body = []
        for notice in Notice.objects.exclude(delivered_at__isnull=False):
            body.append((
                notice.pk,
                notice.kind.code,
                notice.member,
                notice.reference_date,
                notice.status(),
            ))
        print(as_table(headers, body))

    def do_run(self, *args, **options):
        for notice in Notice.objects.filter(send_at=None):
            print(notice, notice.kind, notice.member)
            task_send_notice.delay(notice)
            notice.send_at = timezone.now()
            notice.save()

    def do_before7d(self, *args, **options):
        is_verbose = options.get('verbose')
        is_check = options.get('check')
        kind = NoticeKind.objects.get(app='members', code='before7d')
        members = members_nearly_expired(days=7)
        if not members:
            if is_verbose:
                print("No hay miembros que caduquen en 7 días o menos")
            return
        headers = ['Id.', 'Nombre', 'Válido hasta', 'Estado']
        body = []
        for member in members:
            notice = kind.notice_has_been_send(member, member.valid_until)
            if not notice:
                if is_check:
                    status = green("[Notice would be sent]")
                else:
                    kind.send_notice(member, member.valid_until)
                    status = cyan("[Notice sent]")
            else:
                status = green("[Skipped]")
            body.append((
                    member.pk,
                    member,
                    member.valid_until,
                    status,
                    ))
        print(as_table(headers, body))

    def handle(self, *args, **options):
        subcommand = options.get('subcommand')
        do_callable = getattr(self, f'do_{subcommand}')
        do_callable(*args, **options)
