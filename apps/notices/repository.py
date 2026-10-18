'''
Este fichero mantiene el repositorio de funciones para tipos de avisos.
Para incorporar una función de aviso, añade la correspondiente entrada en
/admin/notices/noticekind/ y escribe en este fichero la función que indiques
en la base de datos.

Cada función debe ser un generador que devuelva una tupla con dos elementos:
- Fecha de referencia del aviso.
- Miembro al que notificar.
'''
import datetime
import logging

from django.db.models import Max
from django.utils import timezone

from apps.members.models import Member
from apps.members.models import Position

logger = logging.getLogger(__name__)


def autotest(days=0):
    logger.info("autotest starts")
    testers = [_.member for _ in Position.objects.actives()]
    hoy = timezone.now().date()
    for member in testers:
        yield hoy, member


def members_nearly_expired(days=0):
    logger.info("members_nearly_expired starts")
    hoy = timezone.now().date()
    if days <= 0:
        from_date = hoy
        to_date = hoy + datetime.timedelta(days=-days + 1)
    else:
        from_date = hoy + datetime.timedelta(days=days)
        to_date = from_date + datetime.timedelta(days=12)
    qs = (
        Member.objects.annotate(max_valid_until=Max('membership__valid_until'))
        .filter(max_valid_until__isnull=False)
        .filter(max_valid_until__gte=from_date)
        .filter(max_valid_until__lt=to_date)
    )
    for m in qs:
        yield m.max_valid_until, m


def all_members(days=0):
    logger.info('all_members starts')
    today = timezone.now().date()
    for member in Member.objects.all():
        yield today, member


def active_members(days=0):
    logger.info('active_members starts')
    today = timezone.now().date()
    for member in Member.objects.all():
        if member.active:
            yield today, member
