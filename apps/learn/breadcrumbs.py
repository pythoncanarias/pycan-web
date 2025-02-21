#!/usr/bin/env python3

from html import escape

from django.urls import reverse_lazy

from apps.commons.breadcrumbs import HOMEPAGE


def bc_root():
    return HOMEPAGE.step(
        'Aprender python',
        reverse_lazy('learn:index'),
        )


def bc_label(label):
    return bc_root().step(
        str(label),
        reverse_lazy('learn:resources_by_label', kwargs={
            'label': label,
            })
        )
