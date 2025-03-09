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
        'is_bound': field.form.is_bound,
        }


@register.inclusion_tag("controls/email_field.html")
def email_field(field, **kwargs):
    control_id = kwargs.pop('id', f'id_{field.name}')
    placeholder = kwargs.pop('placeholder', '')
    return {
        'control_id': control_id,
        'placeholder': placeholder,
        'field': field,
        'is_bound': field.form.is_bound,
        }


@register.inclusion_tag("controls/tel_field.html")
def tel_field(field, **kwargs):
    control_id = kwargs.pop('id', f'id_{field.name}')
    placeholder = kwargs.pop('placeholder', '')
    return {
        'control_id': control_id,
        'placeholder': placeholder,
        'field': field,
        'is_bound': field.form.is_bound,
        }


@register.inclusion_tag("controls/checkbox_field.html")
def checkbox_field(field, **kwargs):
    control_id = kwargs.pop('id', f'id_{field.name}')
    value = kwargs.pop('value', '0')
    checked = kwargs.pop('checked', False)
    return {
        'control_id': control_id,
        'field': field,
        'value': value,
        'checked': checked,
        'is_bound': field.form.is_bound,
        }
