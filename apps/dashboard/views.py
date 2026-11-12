#!/usr/bin/env python3

from datetime import timedelta as TimeDelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from . import breadcrumbs
from . import forms
from apps.members.models import Member


@login_required
def index(request):
    active_members = Member.objects.actives()
    now = timezone.now()
    ref = now - TimeDelta(days=91)
    to_renew = active_members.filter(valid_until__gt=ref)
    return render(request, 'dashboard/index.html', {
        'titulo': f"Dashboard [{request.user}]",
        'breadcrumbs': breadcrumbs.bc_dashboard(),
        'total_active_members': active_members.count(),
        'total_renew_members': to_renew.count(),
        })


@login_required
def new_member(request):
    now = timezone.now()
    form = forms.NewMemberForm()
    return render(request, 'dashboard/new-member.html', {
        'titulo': f"Alta de un nuevo socio",
        'breadcrumbs': breadcrumbs.bc_new_member(),
        'form': form,
        })
