import datetime
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import UploadedFile
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from apps.locations.models import Venue
from apps.quotes.models import Author
from apps.organizations.models import Organization
from apps.members.models import Role, Member, Membership, Position


OK = "\u001b[32m ✓\u001b[0m"


def add_quotes():
    """
    Add a few quotes to have the start page populated with some content
    """
    print("Adding initial quotes", end=" ")
    author, created = Author.objects.get_or_create(
        name='Albert',
        surname='Einstein',
        defaults={
            "url": 'https://es.wikipedia.org/wiki/Albert_Einstein',
            },
    )
    if created:
        quotes = [
            'La imaginación es más importante que el conocimiento. El'
            ' conocimiento es limitado. La imaginación rodea al mundo.',

            'No entiendes realmente algo a menos que seas capaz de'
            ' explicárselo a tu abuela.',

            'Todos somos muy ignorantes, lo que ocurre es que no todos'
            ' ignoramos las mismas cosas.',
            ]
        for quote_text in quotes:
            author.quote_set.create(text=quote_text)
            print(".", end="", flush=True)
    print(OK)


def add_own_organization():
    """
    Add the Python Canarias organization, which is key to make some parts of
    the page work.
    """
    print("Adding own organization", end=" ")
    _, created = Organization.objects.get_or_create(
        name=settings.ORGANIZATION_NAME,
        defaults={
            "cif": 'G76785328',
            "address": 'Calle Albert Einstein, 2',
            "po_box": '28000',
            "city": 'Santa Cruz de Tenerife',
            "bank": 'Banco Bueno',
            "iban": 'ES12 3456 7890 1212 3456 7890',
            "registration_number": '000000001',
        }
    )
    if created:
        print(".", end="", flush=True)
    print(OK)


def add_events():
    """
    Add a sample value and event so we get some content in the events page
    """
    print("Adding sample venue & event", end=" ")
    casa_chano, created = Venue.objects.get_or_create(slug='casa-chano', defaults={
        "name": 'Casa Chano',
        "latitude": 28.4933767,
        "longitude": -16.3782468,
        "website": 'https://casachano.example.com',
        "description": 'Bocadillos',
        "address": 'Calle Secreta, 44, Guamasa'
        }
    )
    if created:
        print(".", end=" ", flush=True)
        # Add photo
        photo_path = Path(settings.BASE_DIR) / 'apps/dev/fixtures/fancy_venue.jpg'
        with photo_path.open('rb') as fin:
            casa_chano.photo = UploadedFile(fin, name=photo_path.name)
            casa_chano.save()
        # Add event
        print("Adding sample event")
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
        print(".", end=" ", flush=True)
    print(OK)


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
        print(".", end=" ", flush=True)
    return user


def load_or_create_role(role_id, name, weigth=100):
    """Get a role by primary key, or create and return a new one
    """
    try:
        result = Role.objects.get(pk=role_id)
    except Role.DoesNotExist:
        print(".", end=" ", flush=True)
        result = Role.objects.create(
            id=role_id,
            role_name=name,
            weigth=weigth,
            )
    return result


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
        print(".", end=" ", flush=True)

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
        print(".", end=" ", flush=True)
    else:
        position.since = membership.valid_from
        position.until = membership.valid_until
        position.save()


def add_board():
    """Adds roles, users, members etc. to get a presentable fake board.
    """
    print("Creating governing board")
    # Creamos al presidente
    print("  - Creating president", end=" ")
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
    print(OK)

    # Creamos a la vicepresidente
    print("  - Creating vicepresident", end=" ")
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
    print(OK)

    # Creamos al secretario
    print("  - Creating secretary", end=" ")
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
    print(OK)

    # Creamos al tesorero
    print("  - Creating treasurer", end=" ")
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
    print(OK)


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
