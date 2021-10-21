import datetime
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.management.base import BaseCommand
from apps.about.models import Ally

from apps.locations.models import Venue
from apps.organizations.models import Organization
from apps.quotes.models import Author


def add_quotes():
    """
    Add a few quotes to have the start page populated with some content
    """
    print("Adding initial quotes")

    author = Author(
        name='Albert',
        surname='Einstein',
        url='https://es.wikipedia.org/wiki/Albert_Einstein',
    )
    author.save()

    quotes = (
        'La imaginación es más importante que el conocimiento. '
        'El conocimiento es limitado. '
        'La imaginación rodea al mundo.',
        'Todos somos muy ignorantes, lo que ocurre es que no todos '
        'ignoramos las mismas cosas.',
    )
    for quote_text in quotes:
        author.quote_set.create(text=quote_text)


def add_own_organization():
    """
    Add the Python Canarias organization, which is key to make some parts of
    the page work.
    """
    print("Adding own organization")
    Organization(
        name=settings.ORGANIZATION_NAME,
        cif='11111111B',
        address='Calle Albert Einstein, 2',
        postal_code='28000',
        city='Santa Cruz de Tenerife',
        bank='Banco Bueno',
        iban='ES12 3456 7890 1212 3456 7890',
        registration_number='000000001',
    ).save()


def add_allies():
    """
    Add the Python Canarias allies, in order to work with this section
    """
    print("Adding allies")

    photo_path = Path(settings.BASE_DIR) / 'apps/dev/fixtures/fancy_venue.jpg'
    with photo_path.open('rb') as fin:
        photo = UploadedFile(fin, name=photo_path.name)
        Ally(
            name='Ally 1',
            description='El aliado 1 es el mejor del mundo',
            logo=photo,
            url='mywebsite.com',
            twitter='https://twitter.com/elonmusk',
            email='some.mail@domain.com',
        ).save()

    photo_path = Path(settings.BASE_DIR) / 'apps/dev/fixtures/avatar.jpg'
    with photo_path.open('rb') as fin:
        photo = UploadedFile(fin, name=photo_path.name)
        Ally(
            name='Un aliado mas',
            description='El aliado 2 no es malo, hace lo que puede',
            logo=photo,
            url='https://domain.me/',
            twitter='https://twitter.com/username',
            email='someone@gmail.com',
        ).save()


def add_events():
    """
    Add a sample value and event so we get some content in the events page
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

    print("Adding sample event")
    casa_chano.events.create(
        name='Pyrriaca',
        hashtag='pyrriaca',
        active=True,
        opened_ticket_sales=False,
        start_date=datetime.date(2023, 9, 23),
        default_slot_duration=datetime.timedelta(minutes=50),
        short_description='Charlas informales de Python',
        description='Bocadillos, vino, y Python, todo opcional menos lo último.',
        closed_schedule=False,
    )


class Command(BaseCommand):
    """
    Add a few entries to the database to allow a minimum developer experience
    """

    help = __doc__

    def handle(self, *args, **options):
        add_own_organization()
        add_quotes()
        add_events()
        add_allies()
