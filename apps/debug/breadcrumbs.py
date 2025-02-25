#!/usr/bin/env python3

from apps.commons.breadcrumbs import HOMEPAGE
from . import links


def bc_root():
    return HOMEPAGE.step(
        'Debug',
        links.to_index(),
        )


def bc_vars():
    return bc_root().step(
        "Variables añadidas al contexto",
        links.to_vars(),
        )


def bc_settings():
    return bc_root().step(
        "Settings",
        links.to_settings(),
        )
