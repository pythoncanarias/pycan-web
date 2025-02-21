#!/usr/bin/env python3

from django.urls import reverse_lazy

from apps.commons.breadcrumbs import HOMEPAGE


def bc_root():
    return HOMEPAGE.step(
        'Sobre nosotros',
        reverse_lazy('about:us'),
        )


def bc_history():
    return bc_root().step(
        'Historia',
        reverse_lazy('about:history'),
        )


def bc_join():
    return bc_root().step(
        'Únete',
        reverse_lazy('about:join'),
        )


def bc_allies():
    return bc_root().step(
        'Aliados',
        reverse_lazy('about:allies'),
        )


def bc_faq():
    return bc_root().step(
        'Preguntas frecuentes',
        reverse_lazy('about:allies'),
        )
