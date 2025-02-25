from django.utils import timezone
from django.conf import settings

from apps.organizations.models import Organization


def global_data(request):
    """Añade al contexto datos de uso general.

    Agrega los datos de:

    - La fecha actual, en `current_date`

    - Los datos de la organización, en `organization`.

    - El valor DEBUG definido en el `settings.py`, en `DEBUG`
    """
    now = timezone.now()
    hoy = now.date()
    return {
        'current_date': hoy,
        'organization': Organization.load_main_organization().to_dict(),
        'DEBUG': settings.DEBUG,
        }
