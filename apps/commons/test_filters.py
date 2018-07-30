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
    assert filters.as_month(2) == 'febrero'
    assert filters.as_month(3) == 'marzo'
    assert filters.as_month(4) == 'abril'
    assert filters.as_month(5) == 'mayo'
    assert filters.as_month(6) == 'junio'
    assert filters.as_month(7) == 'julio'
    assert filters.as_month(8) == 'agosto'
    assert filters.as_month(9) == 'septiembre'
    assert filters.as_month(10) == 'octubre'
    assert filters.as_month(11) == 'noviembre'
    assert filters.as_month(12) == 'diciembre'


def test_as_month_three_letters():
    assert filters.as_month(1, 3) == 'ene'
    assert filters.as_month(2, 3) == 'feb'
    assert filters.as_month(3, 3) == 'mar'
    assert filters.as_month(4, 3) == 'abr'
    assert filters.as_month(5, 3) == 'may'
    assert filters.as_month(6, 3) == 'jun'
    assert filters.as_month(7, 3) == 'jul'
    assert filters.as_month(8, 3) == 'ago'
    assert filters.as_month(9, 3) == 'sep'
    assert filters.as_month(10, 3) == 'oct'
    assert filters.as_month(11, 3) == 'nov'
    assert filters.as_month(12, 3) == 'dic'


# test as_markdown


def test_as_markdown_paragraph():
    assert filters.as_markdown('Hola, mundo.') == '<p>Hola, mundo.</p>\n'


def test_as_markdown_headers():
    assert filters.as_markdown('# Hola, mundo.') == '<h1>Hola, mundo.</h1>\n'
    assert filters.as_markdown('## Hola, mundo.') == '<h2>Hola, mundo.</h2>\n'
    assert filters.as_markdown('### Hola, mundo.') == '<h3>Hola, mundo.</h3>\n'


if __name__ == '__main__':
    pytest.main()
