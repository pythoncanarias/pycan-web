from django.shortcuts import render

from .models import Label


def index(request):
    labels = Label.objects.all()
    return render(request, 'learn/index.html', {'labels': labels})


def resources_by_label(request, label):
    return render(
        request,
        'learn/resources_by_label.html',
        {'label': label, 'resources': label.resources.all()},
    )
