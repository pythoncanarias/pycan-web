import logging
import os
import sys

import django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.organizations.models import Organization

logger = logging.getLogger(__name__)


def index(request):
    pythoncanarias = Organization.objects.get(
        name__istartswith=settings.ORGANIZATION_NAME)
    return render(request, 'about/index.html',
                  {'pythoncanarias': pythoncanarias})


def history(request):
    return render(request, 'about/history.html', {})


@login_required
def versions(request):
    sysname, _, _, version, _ = os.uname()
    info = sys.version_info
    return render(request, "about/versions.html", {
        "titulo": "Control de versiones",
        "os_version": f"{sysname} / {version}",
        "python_version": f"{info.major}.{info.minor}.{info.micro}",
        "django_version": django.__version__,
        }
    )
