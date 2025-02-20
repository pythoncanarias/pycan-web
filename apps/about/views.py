import logging

from django.conf import settings
from django.shortcuts import redirect, render

from .models import Ally, FAQItem
from apps.members.models import Position
from apps.organizations.models import Organization

logger = logging.getLogger(__name__)


def index(request):
    return redirect('about:us')


def us(request):
    positions = [p for p in Position.objects.all() if p.active]
    return render(request, 'about/index.html', {
        'positions': positions,
        })


def join(request):
    organization = Organization.objects.get(
        name__istartswith=settings.ORGANIZATION_NAME
        )
    return render(request, 'about/index.html', {
        'organization': organization,
        'board': Position.get_current_board(),
    })


def history(request):
    return render(request, 'about/history.html', {})


def allies(request):
    allies = Ally.objects.all()
    return render(request, 'about/allies.html', {'allies': allies})


def faq_list(request):
    faqs = FAQItem.objects.order_by('id')
    return render(request, 'about/faq_list.html', {'faqs': faqs})
