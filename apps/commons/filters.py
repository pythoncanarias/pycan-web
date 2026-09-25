'''Remember to register new filters in apps/commons/templatetags/utils.py'''

import datetime
from datetime import datetime as DateTime
from datetime import date as Date
from datetime import timedelta as TimeDelta

from django.utils import timezone
import pytz
from markdown2 import markdown

_MONTHS = [
    '',
    'enero',
    'febrero',
    'marzo',
    'abril',
    'mayo',
    'junio',
    'julio',
    'agosto',
    'septiembre',
    'octubre',
    'noviembre',
    'diciembre',
]

# Mapping from Django Message Tags (https://bit.ly/3gjp5nV)
# into Bulma Notifications (https://bit.ly/3q0fVjH)
BULMA_CLASSES = {
    'debug': 'is-primary',
    'info': 'is-info',
    'success': 'is-success',
    'warning': 'is-warning',
    'error': 'is-danger',
}


def as_month(f: int|Date|DateTime, num_letters=0) -> str:
    n = getattr(f, 'month', f)
    if num_letters:
        return _MONTHS[n][0:num_letters]
    else:
        return _MONTHS[n]


def as_date(f: Date|DateTime) -> str:
    """Fecha o timestamp en formato día/mes/año.

    Ver también: `as_short_date`.

    Ejemplo de uso:

        >>> import datetime
        >>> print(as_date(datetime.date(1992, 1, 2)))
        2/ene/1992
    """
    if isinstance(f, (Date, DateTime)):
        return f'{f.day}/{as_month(f, 3)}/{f.year}'
    return str(f)


def as_short_date(f: Date|DateTime) -> str:
    """Fecha o timestamp en formato día/mes/año.

    Omiten el año si es el mismo del año actual.

    Ver también: `as_date`.

    Ejemplo de uso:

        >>> from datetime import datetime as DateTime
        >>> from datetime import date as Date
        >>> current_year = DateTime.today().year
        >>> print(as_short_date(DateTime(current_year, 1, 2)))
        2/ene
        >>> print(as_short_date(Date(1992, 1, 2)))
        2/ene/1992
    """
    assert isinstance(f, (datetime.date, datetime.datetime))
    today = timezone.now()
    if f.year == today.year:
        return f'{f.day}/{as_month(f, 3)}'
    return f'{f.day}/{as_month(f, 3)}/{f.year}'


def date_from_now(days=1) -> datetime.date:
    today = timezone.now().date()
    delta = TimeDelta(days=days)
    return today + delta


def as_markdown(s: str) -> str:
    result = markdown(s, extras=['tables', 'footnotes'])
    if '<table' in result:
        result = result.replace('<table', '<table class="table"')
    return result


def msgtag_to_bulmaclass(message_tag):
    return BULMA_CLASSES.get(message_tag, 'is-link')


def duration_in_minutes(value):
    return value.seconds // 60


def as_hour(dst: DateTime) -> str:
    """Returns the hours and minutes of a datetime

    It is Normalized if appropriate.
    """
    if dst.tzinfo is not None and dst.tzinfo != pytz.utc:
        dst = pytz.utc.normalize(dst)
    return dst.strftime("%H:%M")
