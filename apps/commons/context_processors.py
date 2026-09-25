
from django.conf import settings
from django.utils import timezone

from apps.organizations.models import Organization


def main_organization_data(request) -> dict:
    return {
        'organization': Organization.load_main_organization(),
        }


def global_data(request):
    """Añade al contexto datos de uso general.

    Agrega los datos de:

    - La fecha actual
    - El valor DEBUG definido en el `settings.py`.
    """
    now = timezone.now()
    hoy = now.date()
    return {
        'current_date': hoy,
        'DEBUG': settings.DEBUG,
        }
