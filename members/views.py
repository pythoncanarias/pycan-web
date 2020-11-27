import logging

from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login

from organizations.models import Organization
from . import forms

logger = logging.getLogger(__name__)


def join(request):
    pythoncanarias = Organization.objects.get(
        name__istartswith=settings.ORGANIZATION_NAME)
    return render(request, 'members/join.html',
                  {'pythoncanarias': pythoncanarias})


def member_login(request):
    """Allows a user to identify himself/herself with the system.
    """
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("/")
    else:
        username = request.GET.get('username', '')
        form = forms.LoginForm(initial={"username": username})
    return render(request, "members/login.html", {
        "title": "Acceder como socio",
        "form": form,
    })


def profile(request: HttpRequest) -> HttpResponse:
    member = request.user.member
    return render(request, "members/profile.html", {
        "title": "Perfil socio {member.pk}: {member.full_name}",
        "member": member,
    })
