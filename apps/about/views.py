import logging

from django.conf import settings
from django.shortcuts import render

from apps.members.models import Position
from apps.organizations.models import Organization

logger = logging.getLogger(__name__)


def index(request):
    positions = [p for p in Position.objects.all() if p.active]
    return render(request, 'about/index.html', {
        'positions': positions,
        })


def join(request):
    pythoncanarias = Organization.objects.get(
        name__istartswith=settings.ORGANIZATION_NAME
    )
    return render(
        request, 'about/join.html', {'pythoncanarias': pythoncanarias}
    )


def history(request):
    return render(request, 'about/history.html', {})
