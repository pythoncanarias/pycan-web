from django.shortcuts import render

from .models import Label


def index(request):
    labels = Label.objects.all()
    return render(request, 'learn/index.html', {'labels': labels})
