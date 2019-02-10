import logging

from django.conf import settings
from django.shortcuts import render

from organizations.models import Organization

logger = logging.getLogger(__name__)


def index(request):
    pythoncanarias = Organization.objects.get(
        name__istartswith=settings.ORGANIZATION_NAME)
    return render(request, 'about/index.html',
                  {'pythoncanarias': pythoncanarias})


def history(request):
    return render(request, 'about/history.html', {})
