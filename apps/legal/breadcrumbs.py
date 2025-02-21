#!/usr/bin/env python3

from html import escape

from django.urls import reverse_lazy

from apps.commons.breadcrumbs import HOMEPAGE


def bc_root():
    return HOMEPAGE.step(
        'Aviso Legal',
        reverse_lazy('legal:legal_notice'),
        )


def bc_coc(language='es'):
    if language == 'en':
        return bc_root().step(
            'Code of conduct',
            reverse_lazy('legal:coc_english'),
            )
    elif language == 'es':
        return bc_root().step(
            'Código de conducta',
            reverse_lazy('legal:coc'),
            )
    raise ValueError(
        f'El código de lenguaje {escape(language)} no es válido.'
        ' Por ahora solo esta disponible esta página en'
        ' inglés y en español'
        )


def bc_privacy_policy():
    return bc_root().step(
        'Privacidad y protección de datos',
        reverse_lazy('legal:purchase_terms'),
        )


def bc_purchase_terms():
    return bc_root().step(
        'Condiciones generales de compra',
        reverse_lazy('legal:purchase_terms'),
        )


def bc_cookie_policy():
    return bc_root().step(
        'Política de cookies',
        reverse_lazy('legal:cookie_policy'),
        )

