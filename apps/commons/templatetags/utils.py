import re

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.commons import filters


def compose2(f, g):
    return lambda x: f(g(x))


register = template.Library()

register.filter('as_month', filters.as_month)
register.filter('as_short_date', filters.as_short_date)
register.filter('as_date', filters.as_date)
register.filter('date_from_now', filters.date_from_now)
register.filter('get_key', filters.get_key)
register.filter('as_markdown', compose2(mark_safe, filters.as_markdown))
register.filter('sum_float', filters.sum_float)
register.filter('startswith', filters.startswith)
register.filter('msgtag_to_bulmaclass', filters.msgtag_to_bulmaclass)
register.filter('duration_in_minutes', filters.duration_in_minutes)

#: Words to be considered like ``False``.
NEGATIVE_VALUES = {
    '0',
    'F',
    'FALSE',
    'INACTIVE',
    'N',
    'NEVER',
    'NO',
    'NOT',
    'NONE',
    'OFF',
    }

@register.filter
def as_boolean(value, options=None):
    """
    Returns a textual representation of a boolean in HTML.

    Unlike Python, a non-empty string could still be treated as
    ``False`` if is in a list of reserved words, like ``'N'``, ``'no'``,
    ``'not'`` ``'False'``, and others.  This is useful for values
    retrieved from configuration files, line ``.ini`` o ``.env``.

    If ``value`` is ``None``, returns ``N/A`` (Does Not Apply).

    .. note::

        List of reserved words to be considered as negatives is in
        contant ``NEGATIVE_VALUES``.

    Use examples:

        >>> assert as_boolean('False') == as_boolean(False)
        >>> assert as_boolean('False', 'OK,ERROR') == 'ERROR'
        >>> assert as_boolean(True, 'OK,ERROR') == 'OK'

    Params:

        value (Any): Value to be interpreted as a boolean. Could
          be any kind, and truey/falsey rules from python still
          apply, with the exception of a reduced set of words, as
          explained.

        options (str): Optional. If used, must be a string that follows
          one of this formats:

            * ``<Yes>``
            * ``<Yes>,<Not>``
            * ``<Yes>,<Not>,<Does not apply>``

    """
    _if_true = '<strong class="boolean yes" style="color: #18442D">\u2705 Sí</strong>'
    _if_false = '<strong class="boolean no" style="color: #321A22">\u274C No</strong>'
    _if_does_not_apply = '<strong class="boolean" style="color: #9E9E9E">N/A</strong>'
    if options:
        if ',' not in options:
            _if_true = options
        else:
            _if_true, _rest = options.split(',', 1)
            if ',' in _rest:
                _if_false, _if_does_not_apply = _resto.split(',', 1)
            else:
                _if_false = _if_does_not_apply = _rest
    if value is None:
        return _if_does_not_apply
    if isinstance(value, str):
        if value.upper() in NEGATIVE_VALUES:
            return _if_false
    return mark_safe(_if_true if bool(value) else _if_false)



@register.simple_tag(takes_context=True)
def is_active(context, named_url):
    """Check if the current url is "under" named_url argument"""
    path = context['request'].path
    url = '^' + reverse(named_url)
    if re.search(url, path):
        return 'is-active'
    else:
        return ''


@register.inclusion_tag('includes/error_list.html')
def error_list(field):
    print(field, type(field))
    return {
        'errors': field.errors,
    }
