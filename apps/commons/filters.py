'''Remember to register new filters in apps/commons/templatetags/utils.py'''

import datetime
from typing import Union

from markdown2 import markdown

_months = [
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


def as_month(f, num_letters=0):
    global _months
    n = getattr(f, 'month', f)
    if num_letters:
        return _months[n][0:num_letters]
    else:
        return _months[n]


def as_date(f: Union[datetime.date, datetime.datetime]) -> str:
    """Fecha o timestamp en formato día/mes/año.

    Ver también: `as_short_date`.

    Ejemplo de uso:

        >>> import datetime
        >>> print(as_date(datetime.date(1992, 1, 2)))
        2/ene/1992
    """
    if isinstance(f, (datetime.date, datetime.datetime)):
        return f'{f.day}/{as_month(f, 3)}/{f.year}'
    return str(f)


def as_short_date(f: Union[datetime.date, datetime.datetime]) -> str:
    """Fecha o timestamp en formato día/mes/año, omitiendo el
    año si es el mismo del año actual.

    Ver también: `as_date`.

    Ejemplo de uso:

        >>> import datetime
        >>> current_year = datetime.date.today().year
        >>> print(as_short_date(datetime.date(current_year, 1, 2)))
        2/ene
        >>> print(as_short_date(datetime.date(1992, 1, 2)))
        2/ene/1992
    """
    if isinstance(f, (datetime.date, datetime.datetime)):
        today = datetime.date.today()
        if f.year == today.year:
            return f'{f.day}/{as_month(f, 3)}'
        return f'{f.day}/{as_month(f, 3)}/{f.year}'
    return str(f)


def date_from_now(days=1) -> datetime.date:
    today = datetime.date.today()
    delta = datetime.timedelta(days=days)
    return today + delta


def get_key(dictionary, key):
    return dictionary.get(key, "")


def as_markdown(s):
    result = markdown(s, extras=['tables', 'footnotes'])
    if '<table' in result:
        result = result.replace('<table', '<table class="table"')
    return result


def sum_float(first_number, second_number):
    return float(first_number) + float(second_number)


def startswith(value, argument):
    return value.startswith(argument)


def msgtag_to_bulmaclass(message_tag):
    return BULMA_CLASSES.get(message_tag, 'is-link')


def duration_in_minutes(value):
    return value.seconds // 60
