#!/usr/bin/env python3

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from apps.certificates.models import Certificate, Attendee
from apps.certificates.models import issue_certificate_for_attendee
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
        'pending_certificates': Attendee.objects.filter(issued_at=None).count(),
        'total_certificates': Attendee.objects.count(),
        })


def list_members(request, *args, **kwargs):
    return render(request, 'dashboard/list_members.html', {
        'title': 'Miembros - Dashboard',
        'members': Member.objects.all(),
        })


def demo(request):
    return render(request, 'dashboard/demo.html', {
        'title': 'Dashboard',
        })


def all_certificates(request):
    certificates = (
        Attendee.objects
        .select_related('event')
        )
    return render(request, "dashboard/certificates.html", {
        'title': 'Todos los certificados',
        'subtitle': 'Ya emitidos o pendientes',
        'attendees': certificates.all(),
        'num_certificates':  certificates.count(),
        })


def list_certificates(request):
    pending_certificates = (
        Attendee.objects
        .filter(issued_at=None)
        .select_related('event')
        )
    return render(request, "dashboard/certificates.html", {
        'attendees': pending_certificates.all(),
        'num_certificates':  pending_certificates.count(),
        })


def view_certificate(request, id_certificate):
    certificate = Certificate.load_certificate(id_certificate)
    attendees = certificate.event.attendees.all()
    return render(request, "dashboard/attendees.html", {
        'certificate': certificate,
        'attendees': attendees,
        })


def issue_certificates(request, id_certificate):
    attendee = Attendee.load_attendee(id_certificate)
    certificates = Certificate.objects.filter(event=attendee.event)
    return render(request, "dashboard/issue_certificates.html", {
        'title': 'Expedir certificados de asistencia',
        'attendee': attendee,
        'certificates': certificates,
        })


def issue_certificate_attendee(request, id_certificate, id_attendee):
    attendee = Attendee.load_attendee(id_attendee)
    certificate = Certificate.load_certificate(id_certificate)
    issue_certificate_for_attendee(certificate, attendee)
    return redirect(
        reverse(
            'certificates:download',
            kwargs={'uuid': attendee.uuid}
            )
        )
