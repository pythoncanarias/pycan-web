import logging

from django.conf import settings
from django.shortcuts import render

from apps.organizations.models import Organization
from apps.members.models import Position


logger = logging.getLogger(__name__)


def index(request):
    organization = Organization.objects.get(
        name__istartswith=settings.ORGANIZATION_NAME)
    return render(request, 'about/index.html', {
        'organization': organization,
        'board': Position.get_current_board(),
    })


def history(request):
    return render(request, 'about/history.html', {})
