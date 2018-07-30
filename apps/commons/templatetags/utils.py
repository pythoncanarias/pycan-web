from django import template
from apps.commons import filters

register = template.Library()

register.filter('as_month', filters.as_month)
register.filter('as_date', filters.as_date)
register.filter('get_key', filters.get_key)
register.filter('get_asset_key', filters.get_asset_key)
