#!/usr/bin/env python3

from datetime import datetime as DateTime
from datetime import timedelta as TimeDelta

import pytz


def as_hour(dst: DateTime):
    """Returns the hours and minutes of a datetime (Normalized if appropriate)
    """
    if dst.tzinfo is not None and dst.tzinfo != pytz.utc:
        dst = pytz.utc.normalize(dst)
    return dst.strftime("%H:%M")


def timestamp(year: int, month: int, day: int, hour=0, minute=0, second=0) -> DateTime:
    """Returns the specified timestamp, in UTC.

    Params:

        year (int): The year
        year (int): The year
        day (int): The day
        hour (int): The hour
        minute (int): The minute
        second (int): The second

    Returns

        An instance ot a DateTime (datetime.datetime) whit the UTC timezone.

    """
    return DateTime(
        year, month, day,
        hour, minute, second,
        tzinfo=pytz.utc
        )


def now() -> DateTime:
    """Returns the current timestamp, in UTC.
    """
    return DateTime.now(pytz.utc)


def now_plus(ref=None, days=0, hours=0, minutes=0, seconds=0):
    """Returns the timestamp, plus an offset, in UTC.

    params:

        ref (DateTime): Optional. A DateTime of referente. Default is the current timestamp
        day (int): Optional. The days to add. Default is 0.
        hour (int): Optional. The hours to add. Default is 0.
        minute (int): Optional. The minutes to add. Default is 0.
        second (int): Optional. The second to add. Default is 0.

    returns:

        A new DateTime, from the ref plus the offset, in the UTC timezone.
    """
    if ref is None:
        ref = now()
    else:
        if ref.tzinfo is not None and ref.tzinfo != pytz.utc:
            ref = pytz.utc.normalize(ref)
    delta = TimeDelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return ref + delta
