#!/usr/bin/env python3

from django.urls import reverse_lazy

from apps.commons.breadcrumbs import HOMEPAGE
from . import links

def bc_root():
    return HOMEPAGE.step(
        'Dashboard',
        links.to_dashboard(),
        )

