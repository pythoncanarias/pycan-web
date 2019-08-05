#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime

from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

from . import crypt, invitation, notification
from .forms import NewMemberForm
from .models import Member


logger = logging.getLogger(__name__)


def index(request):
    today = datetime.date.today()
    members = (
        Member.objects.all()
        .select_related('user')
        .filter(member_until__gt=today)
        .order_by('user__first_name', 'user__last_name')
        )
    return render(request, 'members/index.html', {
        'members': members,
        'today': today,
        })


def new_member(request):
    def get_full_confirmation_url(key):
        encrypted_key = crypt.encrypt(key.bytes).decode()
        confirmation_path = reverse(
            'members:member_confirmation',
            kwargs={'encrypted_key': encrypted_key})
        return f'https://{settings.DOMAIN}{confirmation_path}'

    form = NewMemberForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            payload = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': email,
                'password': form.cleaned_data['password'],
            }
            key = invitation.save_invitation(**payload)
            confirmation_url = get_full_confirmation_url(key)
            notification.send_invitation.delay(confirmation_url, email)
            resp = redirect('members:invited')
            resp.set_cookie('pycan.invited.email', email)
            return resp
    return render(request, 'members/new-member.html', {'form': form})


def member_confirmation(request, encrypted_key):
    pass


def invited(request):
    email = request.COOKIES.get('pycan.invited.email')
    return render(request, 'members/invited.html', {
        'email': email,
    })
