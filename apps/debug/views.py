#!/usr/bin/env python3

import sys
import getpass
import socket
import platform
import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . import breadcrumbs


@login_required
def index(request):
    return render(request, 'debug/index.html', {
        "title": 'Debug data',
        "subtitle": 'Información sobre el sistema',
        "breadcrumbs": breadcrumbs.bc_root(),
        "values": {
            "platorm_architecture": platform.architecture,
            "hostname": socket.gethostname(),
            "os_user": getpass.getuser(),
            "python_version": sys.version,
            "default_encoding": sys.getdefaultencoding(),
            "current_directory": os.getcwd(),
            "path": sys.path,
            },
    })


@login_required
def context_processor_vars(request):
    return render(request, 'debug/context_processor_vars.html', {
        "title": 'Context processro data',
        "subtitle": 'Variables añadidas al contexto',
        "breadcrumbs": breadcrumbs.bc_vars(),
        })


@login_required
def settings(request):
    from django.conf import settings
    return render(request, 'debug/settings.html', {
        "title": 'Django Settings',
        "breadcrumbs": breadcrumbs.bc_settings(),
        "settings": settings,
        })
