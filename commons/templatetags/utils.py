import re

from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse

from commons import filters


def compose2(f, g):
    return lambda x: f(g(x))


register = template.Library()

register.filter('as_month', filters.as_month)
register.filter('as_date', filters.as_date)
register.filter('date_from_now', filters.date_from_now)
register.filter('get_key', filters.get_key)
register.filter('get_asset_key', filters.get_asset_key)
register.filter('as_markdown', compose2(mark_safe, filters.as_markdown))
register.filter('sum_float', filters.sum_float)


@register.simple_tag(takes_context=True)
def is_active(context, named_url):
    """Check if the current url is "under" named_url argument"""
    path = context['request'].path
    url = '^' + reverse(named_url)
    if re.search(url, path):
        return 'is-active'
    else:
        return ''
