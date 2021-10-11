import logging

from django.shortcuts import redirect, render

from apps.members.models import Position

logger = logging.getLogger(__name__)


def index(request):
    return redirect('about:us')


def us(request):
    positions = [p for p in Position.objects.all() if p.active]
    return render(
        request,
        'about/index.html',
        {
            'positions': positions,
        },
    )


def join(request):
    return render(request, 'about/join.html')


def history(request):
    return render(request, 'about/history.html', {})
