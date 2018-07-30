#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
from django.conf import settings


_months = [
    '',
    'enero', 'febrero', 'marzo', 'abril',
    'mayo', 'junio', 'julio', 'agosto',
    'septiembre', 'octubre', 'noviembre', 'diciembre',
]


def as_month(f, num_letters=0):
    global _months
    n = getattr(f, 'month', f)
    if num_letters:
        return _months[n][0:num_letters]
    else:
        return _months[n]


def as_date(f):
    today = datetime.date.today()
    if f.year == today.year:
        return '{}/{}'.format(f.day, as_month(f, 3))
    else:
        return '{}/{}/{}'.format(f.day, as_month(f, 3), f.year)


def get_key(dictionary, key):
    return dictionary.get(key, "")

def get_asset_key(dictionary, key):
    return os.path.join(settings.STATIC_URL, dictionary.get(key, "") or key)
