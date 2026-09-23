import logging

from django.shortcuts import redirect, render
from django.conf import settings

from apps.members.models import Position

from . import models
from . import breadcrumbs

logger = logging.getLogger(__name__)


def index(request):
    return redirect('about:us')


def us(request):
    positions = [p for p in Position.objects.all() if p.active]
    return render(request, 'about/index.html', {
        'titulo': "La asociación",
        'subtitulo': settings.ORGANIZATION_NAME,
        'breadcrumbs': breadcrumbs.bc_us(),
        'positions': positions,
        },
    )


def join(request):
    return render(request, 'about/join.html', {
        'titulo': f"Únete a {settings.ORGANIZATION_NAME}",
        'breadcrumbs': breadcrumbs.bc_join(),
        })


def join_method(request):
    return render(request, 'about/join_method.html', {
        'titulo': f"Únete a {settings.ORGANIZATION_NAME}",
        'breadcrumbs': breadcrumbs.bc_join_method(),
        })


def history(request):
    return render(request, 'about/history.html', {
        'titulo': "Historia de la asociación Python Canarias",
        'breadcrumbs': breadcrumbs.bc_history(),
        })


def allies(request):
    allies = models.Ally.objects.all()
    return render(request, 'about/allies.html', {
        'titulo': "Aliados - Python Canarias",
        'breadcrumbs': breadcrumbs.bc_allies(),
        'allies': allies,
        })


def faq_list(request):
    faqs = models.FAQItem.objects.order_by('id')
    return render(request, 'about/faq_list.html', {
        'titulo': "Preguntas frecuentes sobre Python Canarias",
        'breadcrumbs': breadcrumbs.bc_faq(),
        'faqs': faqs,
        })
