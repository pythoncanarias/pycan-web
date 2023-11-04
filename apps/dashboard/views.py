#!/usr/bin/env python3

from django.shortcuts import render


def index(request, *args, **kwargs):
    return render(request, 'dashboard/index.html', {
        'title': 'Dashboard',
        })


def demo(request):
    return render(request, 'dashboard/demo.html', {
        'title': 'Dashboard',
        })
