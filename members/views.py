import logging

from django.conf import settings
from django.shortcuts import render

from organizations.models import Organization

logger = logging.getLogger(__name__)


def join(request):
    pythoncanarias = Organization.objects.get(
        name__istartswith=settings.ORGANIZATION_NAME)
    return render(request, 'members/join.html',
                  {'pythoncanarias': pythoncanarias})
