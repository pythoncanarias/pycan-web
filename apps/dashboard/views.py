#!/usr/bin/env python3

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from apps.certificates.models import Certificate, Attendee
from apps.events.models import Event
from apps.jobs.models import JobOffer
from apps.members.models import Member
from apps.members.models import Membership
from apps.quotes.models import Quote


def index(request, *args, **kwargs):
    return render(request, 'dashboard/index.html', {
        'title': 'Dashboard',
        'num_members': Membership.num_active_members(),
        'num_events': Event.objects.count(),
        'num_jobs': JobOffer.actives.count(),
        'num_quotes': Quote.objects.count(),
        'num_certificates': Certificate.objects.all().count(),
        'pending_certificates': Attendee.objects.filter(issued_at=None).count(),
        'total_certificates': Attendee.objects.count(),
        })


def list_members(request, *args, **kwargs):
    return render(request, 'dashboard/list_members.html', {
        'title': 'Miembros - Dashboard',
        'members': Member.objects.all(),
        })


def list_events(request, *args, **kwargs):
    return render(request, 'dashboard/list_events.html', {
        'title': 'Aventos - Dashboard',
        'subtitle': 'Todos los events',
        'events': Event.objects.all(),
        })


def list_certificates(request):
    certificates = (
        Certificate.objects
        .select_related('event')
        .all()
        )
    return render(request, "dashboard/list_certificates.html", {
        'certificates': certificates.all(),
        'num_certificates':  certificates.count(),
        })


def view_certificate(request, id_certificate):
    certificate = Certificate.load_certificate(id_certificate)
    attendees = certificate.attendees.all()
    return render(request, "dashboard/attendees.html", {
        'certificate': certificate,
        'attendees': attendees,
        })


def all_attendees(request):
    attendees = (
        Attendee.objects
        .select_related('certificate')
        .all()
        )
    return render(request, "dashboard/attendees.html", {
        'title': 'Todos los certificados',
        'subtitle': 'Ya emitidos o pendientes',
        'attendees': attendees.all(),
        'num_attendees':  attendees.count(),
        })


def pending_attendees(request):
    attendees = (
        Attendee.objects
        .select_related('certificate')
        .filter(issued_at=None)
        )
    return render(request, "dashboard/attendees.html", {
        'title': 'Todos los certificados',
        'subtitle': 'Pendientes de emisión',
        'attendees': attendees.all(),
        'num_attendees':  attendees.count(),
        })


def issue_attendee(request, id_attendee):
    attendee = Attendee.load_attendee(id_attendee)
    attendee.issue_certificate()
    return redirect(
        reverse(
            'certificates:download',
            kwargs={'uuid': attendee.uuid}
            )
        )
