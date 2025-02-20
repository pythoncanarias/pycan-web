from django.shortcuts import render

from .models import Label


def index(request):
    labels = Label.objects.prefetch_related('resources').all()
    return render(request, 'learn/index.html', {
        'title': 'Aprender Python',
        'labels': labels,
        })


def resources_by_label(request, label):
    resources = label.resources.prefetch_related('labels').all()
    return render(request, 'learn/resources_by_label.html', {
        'label': label,
        'resources': resources,
        })
