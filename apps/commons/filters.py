'''Remember to register new filters in apps/commons/templatetags/utils.py'''

import datetime
import os

from django.conf import settings
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


def as_date(f):
    if not isinstance(f, datetime.date):
        return f

    today = datetime.date.today()
    if f.year == today.year:
        return '{}/{}'.format(f.day, as_month(f, 3))
    else:
        return '{}/{}/{}'.format(f.day, as_month(f, 3), f.year)


def date_from_now(days=1):
    today = datetime.date.today()
    delta = datetime.timedelta(days=days)
    return today + delta


def get_key(dictionary, key):
    return dictionary.get(key, "")


def get_asset_key(dictionary, key):
    return os.path.join(settings.STATIC_URL, dictionary.get(key, "") or key)


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
