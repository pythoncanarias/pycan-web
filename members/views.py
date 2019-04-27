import logging

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse

from . import crypt, invitation, notification
from .forms import NewMemberForm

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'members/index.html', {})


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
            payload = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
            }
            key = invitation.save_invitation(**payload)
            notification.send_invitation.delay(
                confirmation_url=get_full_confirmation_url(key),
                email=payload.get('email'))
    return render(request, 'members/new-member.html', {'form': form})


def member_confirmation(request, encrypted_key):
    pass
