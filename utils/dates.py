#!/usr/bin/env python

from datetime import timedelta as TimeDelta
from datetime import date as Date
from django.utils.timezone import now as just_now


def just_today() -> Date:
    """La fecha de hoy.
    """
    return just_now().date()


def this_year() -> int:
    """
    Devuelve el año actual.
    """
    return just_now().year


def num_days(days=1) -> TimeDelta:
    """Obtener un objeto datetime.timedelta con los días indicados.

    Si no se especifica, devuelve timedelta de un día exacto.
    """
    return TimeDelta(days=days)
