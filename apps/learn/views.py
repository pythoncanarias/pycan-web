from django.shortcuts import render

from .models import Label
from . import breadcrumbs


def index(request):
    labels = Label.objects.prefetch_related('resources').all()
    return render(request, 'learn/index.html', {
        'labels': labels,
        'breadcrumbs': breadcrumbs.bc_learn(),
        })


def resources_by_label(request, label):
    resources = label.resources.prefetch_related('labels').all()
    return render( request, 'learn/resources_by_label.html', {
        'breadcrumbs': breadcrumbs.bc_label(label),
        'label': label,
        'resources': resources,
        })
