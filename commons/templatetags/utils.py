from django import template
from django.utils.safestring import mark_safe

from commons import filters


def compose2(f, g):
    return lambda x: f(g(x))


register = template.Library()

register.filter('as_month', filters.as_month)
register.filter('as_date', filters.as_date)
register.filter('get_key', filters.get_key)
register.filter('get_asset_key', filters.get_asset_key)
register.filter('as_markdown', compose2(mark_safe, filters.as_markdown))
