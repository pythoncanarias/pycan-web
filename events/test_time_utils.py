#!/usr/bin/enb python3

import time_utils
import pytest


def test_now():
    t = time_utils.now()


def test_now_plus():
    ref = time_utils.timestamp(2018, 11, 13, 15, 55, 00)
    f = time_utils.now_plus(ref=ref, days=1, hours=1, minutes=1, seconds=1)
    assert f.day == 14
    assert f.hour == 16
    assert f.minute == 56
    assert f.second == 1


def test_now_plus_always_the_future():
    now = time_utils.timestamp(2018, 11, 13, 15, 55, 00)
    assert now < time_utils.now_plus(seconds=1)
    assert now < time_utils.now_plus(minutes=1)
    assert now < time_utils.now_plus(hours=1)
    assert now < time_utils.now_plus(days=1)


if __name__ == '__main__':
    pytest.main()
