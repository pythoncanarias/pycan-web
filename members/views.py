import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from organizations.models import Organization
from . import forms
from .menu import main_menu

logger = logging.getLogger(__name__)


def homepage(request):
    if request.user.is_anonymous:
        return join(request)
    else:
        return profile(request)


def join(request):
    pythoncanarias = Organization.objects.get(
        name__istartswith=settings.ORGANIZATION_NAME)
    return render(request, 'members/join.html',
                  {'pythoncanarias': pythoncanarias})


def member_login(request: HttpRequest) -> HttpResponse:
    """Allows a user to identify himself/herself with the system.
    """
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect(reverse("members:profile"))
    elif request.method in set(['GET', 'HEAD']):
        username = request.GET.get('username', '')
        form = forms.LoginForm(initial={"username": username})
    else:
        raise PermissionDenied(
            "Only GET, HEAD and POST HTTP verbs are valid here"
            )
    return render(request, "members/login.html", {
        "title": "Acceder como socio",
        "form": form,
    })


def member_logout(request: HttpRequest) -> HttpResponse:
    """Close the authenticated session and log out of the system.
    """
    logout(request)
    return redirect(reverse("members:homepage"))


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """Show user profile and member information.
    """
    member = request.user.member
    return render(request, "members/profile.html", {
        "title": "Perfil socio {member.pk}: {member.full_name}",
        "member": member,
        "menu": main_menu,
    })


@login_required
def view_membership(request: HttpRequest) -> HttpResponse:
    member = request.user.member
    return render(request, "members/membership.html", {
        "title": "Socio {member.pk}: {member.full_name} - Pertenencia",
        "member": member,
        "membership": member.membership_set.all(),
        "menu": main_menu,
    })


@login_required
def password_change(request):
    if request.method == 'GET':
        form = forms.PasswordChangeForm(user=request.user)
    elif request.method == 'POST':
        form = forms.PasswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(request)
            return redirect(reverse('members:profile'))
        else:
            messages.warning(request, "El formulario tiene errores")
    else:
        raise PermissionDenied("Only GET and POST HTTP verbs are valid here")
    return render(request, "members/password-change.html", {
        "title": "Cambio de contraseña",
        "form": form,
        "menu": main_menu,
        })
