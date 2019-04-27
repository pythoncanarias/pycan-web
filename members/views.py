import logging

from django.shortcuts import render

from .forms import NewMemberForm
from . import invitation
from . import notification

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'members/index.html', {})


def new_member(request):
    form = NewMemberForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            payload = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
            }
            invitation.save_invitation(**payload)
            notification.send_invitation(**payload)
    return render(request, 'members/new-member.html', {'form': form})
