#!/usr/bin/env python3

from datetime import timedelta as TimeDelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from . import breadcrumbs
from . import forms
from apps.members.models import add_new_member
from apps.members.models import Member
from apps.notices.models import send_notice_now
from apps.obus import Bus


@login_required
def index(request):
    active_members = Member.objects.actives()
    now = timezone.now()
    ref = now + TimeDelta(days=91)
    to_renew = active_members.filter(valid_until__lt=ref)
    return render(request, 'dashboard/index.html', {
        'titulo': f"Dashboard [{request.user}]",
        'breadcrumbs': breadcrumbs.bc_dashboard(),
        'total_active_members': active_members.count(),
        'total_renew_members': to_renew.count(),
        })


@login_required
def active_members(request):
    members = Member.objects.actives().order_by('-pk')
    return render(request, 'dashboard/active-members.html', {
        'titulo': "Socies en activo",
        'breadcrumbs': breadcrumbs.bc_active_members(),
        'members': members,
        'total_members': members.count(),
        })


@login_required
def new_member(request):
    if request.method == 'POST':
        form = forms.NewMemberForm(request.POST)
        if form.is_valid():
            member, password = add_new_member(
                form.cleaned_data['first_name'],
                form.cleaned_data['last_name'],
                form.cleaned_data['email'],
                form.cleaned_data['username'],
                form.cleaned_data['address'],
                form.cleaned_data['rest_address'],
                form.cleaned_data['postal_code'],
                form.cleaned_data['city'],
                form.cleaned_data['phone'],
                form.cleaned_data['payment_date'],
                form.cleaned_data['payment_reference'],
                )
            Bus(request).pub_new_member(member)
            send_notice_now('new_member', member, password=password)
            return redirect(reverse('dashboard:index'))
    else:
        form = forms.NewMemberForm()
    return render(request, 'dashboard/new-member.html', {
        'titulo': "Alta de un nuevo socio",
        'breadcrumbs': breadcrumbs.bc_new_member(),
        'form': form,
        })
