#!/usr/bin/env python3

from django.urls import reverse_lazy

from apps.commons.breadcrumbs import HOMEPAGE


def bc_root():
    return HOMEPAGE.step(
        'Área de socios',
        reverse_lazy('members:homepage'),
        )


def bc_profile(member):
    return bc_root().step(
        str(member.full_name()),
        reverse_lazy('members:profile'),
        )


def bc_membership(member):
    return bc_profile(member).step(
        "Permanecia",
        reverse_lazy('members:membership'),
        )


def bc_password_change(member):
    return bc_profile(member).step(
        "Cambiar la contraseña",
        reverse_lazy('members:password_change'),
        )


def bc_address_change(member):
    return bc_profile(member).step(
        "Cambiar la dirección",
        reverse_lazy('members:address_change'),
        )


def bc_board():
    return bc_root().step(
        "Junta de gobierno",
        reverse_lazy('members:board'),
        )
