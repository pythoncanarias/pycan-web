#!/usr/bin/env python3

import datetime
import functools
import operator

import pytz


def as_hour(dst):
    """Returns the hours and minutes of a datetime (Normalized if appropriate)
    """
    if dst.tzinfo is not None and dst.tzinfo != pytz.utc:
        dst = pytz.utc.normalize(dst)
    return dst.strftime("%H:%M")


def timestamp(year, month, day, hour, minute, second):
    return datetime.datetime(
        year, month, day,
        hour, minute, second,
        tzinfo=pytz.utc
        )


def now():
    return datetime.datetime.now(pytz.utc)


def now_plus(ref=None, days=0, hours=0, minutes=0, seconds=0):
    if ref is None:
        ref = now()
    else:
        if ref.tzinfo is not None and ref.tzinfo != pytz.utc:
            ref = pytz.utc.normalize(ref)
    steps = [ref]
    if days:
        steps.append(datetime.timedelta(days))
    if hours:
        steps.append(datetime.timedelta(0, 0, 0, 0, 0, hours))
    if minutes:
        steps.append(datetime.timedelta(0, 0, 0, 0, minutes))
    if seconds:
        steps.append(datetime.timedelta(0, seconds))
    return functools.reduce(operator.add, steps)
