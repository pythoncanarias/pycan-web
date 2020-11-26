import logging

from django.conf import settings
from django.shortcuts import render

from organizations.models import Organization
from members.models import Position

logger = logging.getLogger(__name__)


def board(request):
    organization = Organization.objects.get(name=settings.ORGANIZATION_NAME)
    return render(request, 'members/board.html', {
        'organization': organization,
        'board': Position.get_current_board(),
    })


def join(request):
    pythoncanarias = Organization.objects.get(
        name__istartswith=settings.ORGANIZATION_NAME)
    return render(request, 'members/join.html',
                  {'pythoncanarias': pythoncanarias})
