import datetime
import pytest

from . import filters

# as_date


def test_as_date():
    d = datetime.date(2016, 4, 18)
    assert filters.as_date(d) == '18/abr/2016'


def test_as_date_current_year():
    today = datetime.date.today()
    d = datetime.date(today.year, 4, 18)
    assert filters.as_date(d) == '18/abr'


# as_month

def test_as_month():
    assert filters.as_month(1) == 'enero'
    assert filters.as_month(12) == 'diciembre'


def test_as_month_three_letters():
    assert filters.as_month(1, 3) == 'ene'
    assert filters.as_month(12, 3) == 'dic'


if __name__ == '__main__':
    pytest.main()
