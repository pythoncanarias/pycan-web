from django.shortcuts import render

from . import models
from . import breadcrumbs

def index(request):
    labels = models.Label.objects.prefetch_related('resources').all()
    return render(request, 'learn/index.html', {
        'title': 'Aprender Python',
        'breadcrumbs': breadcrumbs.bc_root(),
        'labels': labels,
        })


def resources_by_label(request, label):
    resources = label.resources.prefetch_related('labels').all()
    return render(request, 'learn/resources_by_label.html', {
        'title': 'Aprender python',
        'subtitle': str(label),
        'label': label,
        'breadcrumbs': breadcrumbs.bc_label(label),
        'resources': resources,
        })
