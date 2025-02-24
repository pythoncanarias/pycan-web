#!/usr/bin/env python3

from django import template

register = template.Library()


@register.inclusion_tag("controls/text_field.html")
def text_field(field, **kwargs):
    control_id = kwargs.pop('id', f'id_{field.name}')
    placeholder = kwargs.pop('placeholder', '')
    return {
        'control_id': control_id,
        'placeholder': placeholder,
        'field': field,
        }


@register.inclusion_tag("controls/email_field.html")
def email_field(field, **kwargs):
    control_id = kwargs.pop('id', f'id_{field.name}')
    placeholder = kwargs.pop('placeholder', '')
    return {
        'control_id': control_id,
        'placeholder': placeholder,
        'field': field,
        }


@register.inclusion_tag("controls/tel_field.html")
def tel_field(field, **kwargs):
    control_id = kwargs.pop('id', f'id_{field.name}')
    placeholder = kwargs.pop('placeholder', '')
    return {
        'control_id': control_id,
        'placeholder': placeholder,
        'field': field,
        }
