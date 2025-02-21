import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from . import forms
from . import breadcrumbs
from . import menu
from apps.organizations.models import Organization


logger = logging.getLogger(__name__)


def homepage(request):
    return redirect('members:profile')


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """Show user profile and member information.
    """
    member = request.user.member
    return render(request, "members/profile.html", {
        "title": member.full_name(),
        "subtitle": f"Socio núm. {member.pk}",
        "breadcrumbs": breadcrumbs.bc_profile(member),
        "member": member,
        "menu": menu.main_menu,
        })


def member_login(request: HttpRequest) -> HttpResponse:
    """Allows a user to identify himself/herself with the system."""
    if request.user.is_authenticated:
        return redirect(reverse('members:profile'))
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect(reverse("members:profile"))
        else:
            messages.error(request, "El formulario tiene errores")
    elif request.method in set(['GET', 'HEAD']):
        username = request.GET.get('username', '')
        form = forms.LoginForm(initial={"username": username})
    else:
        raise PermissionDenied(
            "Only GET, HEAD and POST HTTP verbs are valid here"
        )
    return render(
        request,
        "members/login.html",
        {
            "title": "Acceder como socio",
            "form": form,
        },
    )


def member_logout(request: HttpRequest) -> HttpResponse:
    """Close the authenticated session and log out of the system."""
    logout(request)
    return redirect(reverse("members:homepage"))


@login_required
def view_membership(request: HttpRequest) -> HttpResponse:
    member = request.user.member
    return render(request, "members/membership.html", {
        "title": member.full_name(),
        "subtitle": "Pertenencia",
        "breadcrumbs": breadcrumbs.bc_membership(member),
        "member": member,
        "membership": member.membership_set.all(),
        "menu": menu.main_menu,
        })


@login_required
def password_change(request):
    member = request.user.member
    if request.method == 'GET':
        form = forms.PasswordChangeForm(user=request.user)
    elif request.method == 'POST':
        form = forms.PasswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(request)
            return redirect(reverse('members:profile'))
        else:
            messages.error(request, "El formulario tiene errores")
    else:
        raise PermissionDenied("Only GET and POST HTTP verbs are valid here")
    return render(request, "members/password-change.html", {
        "title": member.full_name(),
        "subtitle": "Cambio de contraseña",
        "breadcrumbs": breadcrumbs.bc_password_change(member),
        "form": form,
        "menu": menu.main_menu,
        })


@login_required
def address_change(request):
    member = request.user.member
    if request.method == 'POST':
        form = forms.ChangeAddressForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('members:profile'))
        messages.error(request, 'El formulario tiene errores')
    else:
        form = forms.ChangeAddressForm(instance=member)
    return render(request, 'members/address-change.html', {
        'title': member.full_name(),
        'subtitle': 'Cambio de dirección',
        'breadcrumbs': breadcrumbs.bc_address_change(member),
        'form': form,
        "menu": menu.main_menu,
        })



def join(request):
    pythoncanarias = Organization.objects.get(name__istartswith=settings.ORGANIZATION_NAME)
    return render(request, 'members/join.html', {
        'pythoncanarias': pythoncanarias,
        })
