import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.members.models import Member
from . import breadcrumbs
from . import forms
from . import menu

logger = logging.getLogger(__name__)


@login_required
def homepage(request: HttpRequest) -> HttpResponse:
    """Show user profile and member information.
    """
    member = request.user.member
    return render(request, "members/homepage.html", {
        'titulo': "Perfil socio {member.pk}: {member.full_name}",
        'breadcrumbs': breadcrumbs.bc_members(),
        'member': member,
        'menu': menu.main_menu(request),
        })



def member_login(request: HttpRequest) -> HttpResponse:
    """Allows a user to identify himself/herself with the system."""
    if request.user.is_authenticated:
        return redirect(reverse('members:homepage'))
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect(reverse("members:homepage"))
        else:
            messages.error(request, "El formulario tiene errores")
    else:
        username = request.GET.get('username', '')
        form = forms.LoginForm(initial={"username": username})
    return render(request, "members/login.html", {
        "titulo": "Acceder como socio",
        'breadcrumbs': breadcrumbs.bc_members(),
        "form": form,
        })


def member_logout(request: HttpRequest) -> HttpResponse:
    """Close the authenticated session and log out of the system."""
    logout(request)
    return redirect(reverse("homepage"))



@login_required
def membership(request: HttpRequest) -> HttpResponse:
    member = request.user.member
    return render(request, "members/membership.html", {
        "titulo": "Socio {member.pk}: {member.full_name} - Datos de pertenencia",
        'breadcrumbs': breadcrumbs.bc_membership(),
        "member": member,
        "membership": member.membership_set.all(),
        'menu': menu.main_menu(request),
        })


@login_required
def password_change(request):
    if request.method == 'POST':
        form = forms.PasswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(request)
            return redirect(reverse('members:homepage'))
        else:
            messages.error(request, "El formulario tiene errores")
    else:
        form = forms.PasswordChangeForm(user=request.user)
    return render(request, "members/password-change.html", {
        'titulo': "Cambio de contraseña",
        'breadcrumbs': breadcrumbs.bc_password_change(),
        'form': form,
        'menu': menu.main_menu(request),
        })


def address_change(request):
    member = Member.load_from_username(request.user.username)
    if request.method == 'POST':
        form = forms.ChangeAddressForm(request.POST, instance=member)
        if form.is_valid():
            form.save(request)
            return redirect(reverse('members:homepage'))
        else:
            num_errors = sum(len(err) for err in form.errors.values())
            messages.error(
                request,
                f'El formulario tiene {num_errors} errores',
                )
    else:
        form = forms.ChangeAddressForm(instance=member)
    return render(request, 'members/address-change.html', {
        'titulo': "Cambio de dirección",
        'breadcrumbs': breadcrumbs.bc_address_change(),
        'form': form,
        'menu': menu.main_menu(request),
        })
