#!/usr/bin/env python3

from apps.commons.breadcrumbs import HOMEPAGE


def bc_root():
    return HOMEPAGE.step('Aviso Legal', 'legal:index')
