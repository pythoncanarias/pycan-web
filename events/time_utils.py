#!/usr/bin/env python3

from datetime import datetime as timestamp
from datetime import timedelta
from functools import reduce
from operator import add

def now():
    return timestamp.now()


def now_plus(ref=None, days=0, hours=0, minutes=0, seconds=0):
    steps = [ref or now()]
    if days:
        steps.append(timedelta(days))
    if hours:
        steps.append(timedelta(0, 0, 0, 0, 0, hours))
    if minutes:
        steps.append(timedelta(0, 0, 0, 0, minutes))
    if seconds:
        steps.append(timedelta(0, seconds))
    return reduce(add, steps)
