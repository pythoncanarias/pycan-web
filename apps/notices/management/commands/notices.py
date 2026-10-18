from inspect import getmembers, isfunction

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.utils import timezone

from adapters.console import print, as_table, cyan, green, red, yes_no
from apps.members.models import Member
from apps.notices import repository
from apps.notices.models import Notice, NoticeKind
from apps.notices.tasks import task_send_notice

NOTICE_KIND = dict(getmembers(repository, isfunction))


class Command(BaseCommand):

    help = 'Gestión de avisos a socios'

    def add_arguments(self, parser):
        self.parser = parser
        parser.add_argument('--verbose', action='store_true', help='Verboso')
        subparser = parser.add_subparsers(dest="subcommand")
        # test
        run_parser = subparser.add_parser("test")
        run_parser.add_argument('email', action='store')
        run_parser.add_argument('kind', action='store')
        # run
        run_parser = subparser.add_parser("run")
        run_parser.add_argument('--kind', default='all')
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
            type=str,
            help="Activar un tipo de aviso",
        )
        rules_parser.add_argument(
            '--disable',
            type=str,
            help="Desactivar un tipo de aviso",
        )

    def heading(self, text: str):
        if self.is_verbose:
            self.stdout.write(self.style.MIGRATE_HEADING(text))

    def out(self, text: str):
        self.stdout.write(text)

    def notice(self, text: str):
        if self.is_verbose:
            self.stdout.write(self.style.NOTICE(text))

    def warning(self, text: str):
        self.stdout.write(self.style.WARNING(text))

    def do_test(self, *args, **options):
        self.is_verbose = True
        _email = options.get('email')
        member = Member.load_from_email(_email)
        _kind = options.get('kind')
        kind = NoticeKind.load_notice_kind(_kind)
        ref_date = timezone.now().date()
        notice = kind.enqueue_notice(member, ref_date)
        task_send_notice.delay(notice.pk)
        self.heading(f"Prueba de notificación tipo {kind} a {member}")
        self.out(f"Notice {notice.pk} queued")

    def do_message(self, *args, **options):
        id_notice = options.get('id_notice')
        notice = Notice.load_notice(id_notice)
        self.is_verbose = True
        self.heading(f"Detalles notificación #{id_notice}")
        _to = f"{notice.member.full_name} <{notice.member.email}>"
        self.out(f'Para    : {_to}')
        self.out(f'subject : {notice.kind.description}')
        self.out(f'status  : {notice.status()}')
        self.out('--[ Cuerpo del mensaje ]-------------------------------')
        self.out(notice.message_text)
        self.out('-------------------------------------------------------')

    def do_list(self, *args, **options):
        num_rows = options.get('num_rows')
        body = [(
                notice.pk,
                notice.member,
                notice.kind,
                notice.reference_date,
                yes_no(notice.status()),
            ) for notice in
            Notice.objects.order_by('-created_at')[0:num_rows]
            ]
        if body:
            headers = [
                'Msg.',
                'Member',
                'Notice',
                'Ref. date',
                'delivered',
                ]
            print(as_table(headers, body))
        else:
            self.warning('No hay ningún aviso en la base de datos')

    def do_rules(self, *args, **options):
        body = []
        id_to_enable = options.get('enable')
        id_to_disable = options.get('disable')
        if id_to_enable and id_to_disable and id_to_enable == id_to_disable:
            # Las dos opciones son mutuamente exclueyentes
            return
        if id_to_enable:
            kind = NoticeKind.load_notice_kind(id_to_enable)
            if kind:
                kind.enable()
        if id_to_disable:
            kind = NoticeKind.load_notice_kind(id_to_disable)
            if kind:
                kind.disable()
        for kind in NoticeKind.objects.all():
            status_code = callable(NOTICE_KIND.get(kind.code))
            body.append(
                (
                    kind.pk,
                    kind.description,
                    kind.template,
                    green(kind.code) if status_code else red(kind.code),
                    kind.days,
                    yes_no(kind.enabled),
                )
            )
        headers = ["Id.", "Description", "Tamplate", "Code", "Days", "Enabled"]
        print(as_table(headers, body))

    def do_run(self, **options):
        is_check = options.get('check')
        kind_option = options.get('kind')
        if kind_option.lower() == 'all':
            kinds = list(NoticeKind.objects.filter(enabled=True).all())
        else:
            kind = NoticeKind.load_notice_kind(kind_option)
            if not kind:
                raise CommandError(
                    'No se ha encontrado ninguna regla'
                    f' por el código indicado {kind_option}.'
                    )
            if not kind.enabled:
                raise CommandError(
                    f'La regla indicada [{kind_option}] no está activa.\n'
                    ' Debe activarla primero para poder ejecutarla. Vea'
                    ' la orden rules.'
                    )
            kinds = [kind]

        body = []
        for kind in kinds:
            self.heading(
                "Procesando notificaciones"
                f" de tipo {kind.code}: {kind.description}"
                )
            code = NOTICE_KIND.get(kind.code)
            if not code:
                raise CommandError(
                    f"No existe el código de la regla {kind.code}"
                    )
            if callable(code):
                for ref_date, member in code(days=kind.days):
                    notice = kind.notice_has_been_send(member, ref_date)
                    if notice:
                        status = green(f"[Skipped {notice.pk}]")
                    else:
                        if is_check:
                            status = green("[Notice would be queued]")
                        else:
                            notice = kind.enqueue_notice(member, ref_date)
                            task_send_notice.delay(notice.pk)
                            status = cyan("[Notice {notice.pk} queued]")
                    body.append((member, kind, ref_date, status))
            else:
                raise CommandError(
                    f"El código de la regla indicado {kind.code}"
                    " no es ejecutable"
                    )
        if self.is_verbose or is_check:
            headers = ['Member', 'Notice', 'Ref. date', 'Status']
            print(as_table(headers, body))

    def handle(self, *args, **options):
        subcommand = options.get('subcommand')
        self.is_verbose = options.get('verbose')
        if subcommand:
            do_cmd = getattr(self, f'do_{subcommand}', None)
            if callable(do_cmd):
                do_cmd(*args, **options)
        else:
            self.parser.print_help()
