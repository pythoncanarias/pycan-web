import logging

from django.shortcuts import redirect, render

from apps.members.models import Position
from apps.organizations.models import Organization
from . import models
from . import breadcrumbs


logger = logging.getLogger(__name__)


def index(request):
    return redirect('about:us')


def us(request):
    organization = Organization.load_main_organization()
    board = Position.get_current_board()
    return render(request, 'about/index.html', {
        'title': 'Sobre la organización',
        'subtitle': str(organization),
        'breadcrumbs': breadcrumbs.bc_root(),
        'board': board,
        })


def join(request):
    organization = Organization.load_main_organization()
    return render(request, 'about/join.html', {
        'title': 'No nos mires, ¡únete!',
        'breadcrumbs': breadcrumbs.bc_join(),
        'board': board,
        'organization': organization,
    })


def history(request):
    organization = Organization.load_main_organization()
    return render(request, 'about/history.html', {
        'title': f'Historia de {organization}',
        'breadcrumbs': breadcrumbs.bc_history(),
        })


def allies(request):
    return render(request, 'about/allies.html', {
        'title': 'Aliados',
        'breadcrumbs': breadcrumbs.bc_allies(),
        'allies': models.Ally.objects.all(),
        })


def faq_list(request):
    return render(request, 'about/faq_list.html', {
        'title': 'Preguntas frecuentes',
        'breadcrumbs': breadcrumbs.bc_faq(),
        'faqs': models.FAQItem.objects.order_by('id'),
        })


def board(request):
    organization = Organization.load_main_organization()
    return render(request, 'about/board.html', {
        'title': 'Datos de la organización',
        'subtitle': str(organization),
        'organization': organization,
        'board': Position.get_current_board(),
        })
