import datetime
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from apps.about.models import Ally, FAQItem
from apps.locations.models import Venue
from apps.organizations.models import Organization
from apps.quotes.models import Author
from apps.members.models import Role, Member, Membership, Position


OK = "\u001b[32m ✓\u001b[0m"


def step_start(title):
    print(title, end=" ")


def step_progress():
    print(".", end="", flush=True)


def step_ok():
    print(OK)


def add_quotes():
    """Add a few quotes to have the start page populated with some content.
    """
    step_start("Adding initial quotes")
    author, created = Author.objects.get_or_create(
        name='Albert',
        surname='Einstein',
        defaults={
            "url": 'https://es.wikipedia.org/wiki/Albert_Einstein',
            },
        )
    if created:
        quotes = (
            'La imaginación es más importante que el conocimiento. '
            'El conocimiento es limitado. '
            'La imaginación rodea al mundo.',
            'Todos somos muy ignorantes, lo que ocurre es que no todos '
            'ignoramos las mismas cosas.',
            'No entiendes realmente algo a menos que seas capaz de'
            ' explicárselo a tu abuela.',
            )
        for quote_text in quotes:
            author.quote_set.create(text=quote_text)
            step_progress()
    step_ok()


def add_own_organization():
    """Add the Python Canarias organization.

    This is key to make some parts of the page work.
    """
    step_start("Adding own organization")
    _, created = Organization.objects.get_or_create(
        name=settings.ORGANIZATION_NAME,
        cif='11111111B',
        address='Calle Albert Einstein, 2',
        postal_code='28000',
        city='Santa Cruz de Tenerife',
        bank='Banco Bueno',
        iban='ES12 3456 7890 1212 3456 7890',
        registration_number='000000001',
    ).save()
    if created:
        step_progress()
    step_ok()


def add_allies():
    """Add the Python Canarias allies.

    In order to work with this section
    """
    print("Adding allies")

    photo_path = Path(settings.BASE_DIR) / 'apps/dev/fixtures/adalovedev.jpg'
    with photo_path.open('rb') as fin:
        photo = UploadedFile(fin, name=photo_path.name)
        Ally(
            name='AdaLoveDev',
            description='Somos una comunidad sin ánimo de lucro cuyo objetivo'
            'es dar visibilidad y empoderamiento a las mujeres en el sector'
            'tecnológico',
            logo=photo,
            url='https://adalovedev.es/',
            twitter='https://twitter.com/adalovedev',
            email='organization@adalovedev.es',
        ).save()

    photo_path = Path(settings.BASE_DIR) / 'apps/dev/fixtures/python-es.png'
    with photo_path.open('rb') as fin:
        photo = UploadedFile(fin, name=photo_path.name)
        Ally(
            name='Python España',
            description='Asociación Python España. Trabajando para promover y'
            'visibilizar el uso del lenguaje de programación Python en nuestro'
            'país',
            logo=photo,
            url='https://www.es.python.org/',
            twitter='https://twitter.com/python_es',
            email=' contacto@es.python.org',
        ).save()


def add_events():
    """Add a sample value and event.

    So we get some content in the events page.
    """
    print("Adding sample venue")
    photo_path = Path(settings.BASE_DIR) / 'apps/dev/fixtures/fancy_venue.jpg'

    with photo_path.open('rb') as fin:
        photo = UploadedFile(fin, name=photo_path.name)
        casa_chano = Venue(
            name='Casa Chano',
            slug='casa-chano',
            latitude=28.4933767,
            longitude=-16.3782468,
            photo=photo,
            website='https://casachano.example.com',
            description='Bocadillos',
            address='Calle Secreta, 44, Guamasa',
        )
        casa_chano.save()

    step_start("Adding sample venue & event")
    casa_chano, created = Venue.objects.get_or_create(slug='casa-chano', defaults={
        "name": 'Casa Chano',
        "latitude": 28.4933767,
        "longitude": -16.3782468,
        "website": 'https://casachano.example.com',
        "description": 'Bocadillos',
        "address": 'Calle Secreta, 44, Guamasa'
        })
    if created:
        step_progress()
        # Add photo
        photo_path = Path(settings.BASE_DIR) / 'apps/dev/fixtures/fancy_venue.jpg'
        with photo_path.open('rb') as fin:
            casa_chano.photo = UploadedFile(fin, name=photo_path.name)
            casa_chano.save()
        # Add event
        casa_chano.events.create(
            name='Pyrriaca',
            hashtag='pyrriaca',
            active=True,
            opened_ticket_sales=False,
            start_date=datetime.date(2023, 9, 23),
            default_slot_duration=datetime.timedelta(minutes=50),
            short_description='Charlas informales de Python',
            description=(
                'Bocadillos, vino, y Python, todo opcional'
                ' menos lo último.'
                ),
            closed_schedule=False
        )
        step_progress()
    step_ok()


def load_or_create_user(username, **kwargs):
    """Get a user based on username, or create and return one if not exists.

    We can't use the objects method `get_or_create`, because `User`
    model has the special `password` field, and needs a customized
    create method.
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username, **kwargs)
        step_progress()
    return user


def load_or_create_role(role_id, name, weight=100):
    """Get a role by primary key, or create and return a new one
    """
    role, created = Role.objects.get_or_create(id=role_id, defaults={
        'role_name': name,
        'weight': weight,
        })
    if created:
        step_progress()
    return role


def assign_role(role, member):
    """Assings a role to a member.

    Force the membership to be valid, if required, as all
    board members must have a valid membership.
    """
    # Create or load membership.
    membership = Membership.objects.last()
    if membership:
        if not membership.is_valid():
            delta = datetime.timedelta(days=91)
            membership.valid_until = datetime.date.today() + delta
            membership.save()
    else:
        date_since = datetime.date.today() - datetime.timedelta(days=1)
        valid_period = datetime.timedelta(days=1462)  # 4 years + 1 day
        date_until = date_since + valid_period
        membership = Membership.objects.create(
            member=member,
            valid_from=date_since,
            valid_until=date_until,
        )
        step_progress()

    # Create or load position
    position, created = Position.objects.get_or_create(
        role=role,
        member=member,
        defaults={
            "since": membership.valid_from,
            "until": membership.valid_until,
        }
    )
    if created:
        step_progress()
    else:
        position.since = membership.valid_from
        position.until = membership.valid_until
        position.save()


def add_board():
    """Adds roles, users, members etc. to get a presentable fake board.
    """
    print("Creating governing board")
    step_start("  - Creating president")
    clark = load_or_create_user(
        'clark_kent',
        email='clark.kent@dailyplanet.com',
        password="ILoveKrypton36",
        first_name="Clark",
        last_name="Kent",
        )
    clark_member, _ = Member.objects.get_or_create(
        user=clark,
        defaults={
            "address": "Solitude Fortress, 1",
            "city": "Metropolis",
            "phone": "111-2222",
            }
        )
    president = load_or_create_role('PRE', "Presidencia", 100)
    assign_role(president, clark_member)
    step_ok()

    step_start("  - Creating vicepresident")
    diana = load_or_create_user(
        'diana_prince',
        email='wonderwoman@justiceleague.org',
        password="Themysc1r4",
        first_name="Diana",
        last_name="Prince",
        )
    diana_member, _ = Member.objects.get_or_create(
        user=diana,
        defaults={
            "address": "Musée du Louvre",
            "rest_address": "75001 Paris, FranceLouvre Museum Manor",
            "city": "Paris",
            "phone": "993-2201-761",
            }
        )
    vicepresident = load_or_create_role('VPR', "Vicepresidencia", 200)
    assign_role(vicepresident, diana_member)
    step_ok()

    step_start("  - Creating secretary")
    barry = load_or_create_user(
        'barry_allen',
        email='barry@ccpd.centralcity.gov',
        password="Fastest Man Alive Showcase 4",
        first_name="Barry",
        last_name="Allen",
        )
    barry_member, _ = Member.objects.get_or_create(
        user=barry,
        defaults={
            "address": "156 Long Street",
            "city": "Central City",
            "phone": "312-2373-876",
            }
        )
    secretary = load_or_create_role('SEC', "Secretaría", 300)
    assign_role(secretary, barry_member)
    step_ok()

    step_start("  - Creating treasurer")
    bruce = load_or_create_user(
        'bruce_wayne',
        email='bruce@waynetech.com',
        password="64181122-60df-46e3-9173-0a4dc1219e62",
        first_name="Bruce",
        last_name="Wayne",
        )
    bruce_member, _ = Member.objects.get_or_create(
        user=bruce,
        defaults={
            "address": "Wayne Manor",
            "city": "Gothan City",
            "phone": "849-4823-312",
            }
        )
    treasurer = load_or_create_role('TRE', "Tesorería", 400)
    assign_role(treasurer, bruce_member)
    step_ok()


def add_faq_items():
    print('Adding sample faq item about Python')
    FAQItem(
        question='¿Qué es Python?',
        answer='''Python es un lenguaje de programación interpretado cuya
filosofía hace hincapié en la legibilidad de su código. Se trata de
un lenguaje de programación multiparadigma, ya que soporta parcialmente la
orientación a objetos, programación imperativa y, en menor medida,
programación funcional. Es un lenguaje interpretado, dinámico y
multiplataforma.''',
    ).save()

    print('Adding sample faq item about Python benefits')
    FAQItem(
        question='¿Es Python un buen lenguaje para empezar a programar?',
        answer='''Sí. Python tiene una sintaxis simple y consistente, dispone
de una librería estándar muy completa. Al ser multiparadigma sirve de
introducción para programación orientada a objetos, funcional y procedural.''',
    ).save()


class Command(BaseCommand):
    """
    Add a few entries to the database to allow a minimum developer experience
    """

    help = __doc__

    def handle(self, *args, **options):
        add_own_organization()
        add_board()
        add_quotes()
        add_events()
        add_allies()
        add_faq_items()

