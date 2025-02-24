#!/usr/bin/env python3

from django.shortcuts import redirect
from django.http import Http404

from apps.certificates.models import Attendee


def download_certificate(request, uuid):
    attendee = Attendee.load_attendee_by_uuid(uuid)
    if attendee:
        return redirect(attendee.pdf.url)
    raise Http404('Certificado no disponible')
