import datetime
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.management.base import BaseCommand

from apps.about.models import Ally, FAQItem
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
        description='Bocadillos, vino y Python, todo opcional menos lo último',
        closed_schedule=False,
    )


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
        add_quotes()
        add_events()
        add_allies()
        add_faq_items()
