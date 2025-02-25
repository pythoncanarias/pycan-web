#!/usr/bin/env python3


from django.urls import reverse_lazy


def to_index():
    return reverse_lazy('debug:index')


def to_vars():
    return reverse_lazy('debug:context_processor_vars')
