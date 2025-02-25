#!/usr/bin/env python3

from django.urls import reverse_lazy


def to_dashboard():
    return reverse_lazy('dashboard:index')
