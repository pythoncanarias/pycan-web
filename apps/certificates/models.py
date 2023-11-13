#!/usr/bin/env python3

import os
from tempfile import NamedTemporaryFile
import subprocess
import uuid

from django.core.files import File
from django.db import models
from django.forms.models import model_to_dict
from django.template import Context, Template
from utils.dates import just_now
from apps.events.models import Event


def _certificates_upload_to(instance, filename):
    return f"events/{instance.event.hashtag}/{filename}"


class Certificate(models.Model):

    class Meta:

        verbose_name = 'certificado'
        verbose_name_plural = 'certificados'
        ordering = ['description']

    description = models.CharField(
        help_text='Description and purpouse of certificate',
        max_length=256,
        )
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name="certificates",
        help_text='This certificate related event',
        )
    template = models.FileField(
        max_length=512,
        upload_to=_certificates_upload_to,
        help_text='Template to be used to generate PDF',
    )
    created_at = models.DateTimeField(auto_now=True)

    @classmethod
    def load_certificate(cls, pk: int):
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return str(self.description)


def _issued_certificates_upload_to(instance, filename):
    public_filename = f'{instance.uuid}.pdf'
    return f"events/{instance.event.hashtag}/{public_filename}"


class Attendee(models.Model):

    class Meta:
        verbose_name = 'asistente'
        verbose_name_plural = 'asistentes'
        ordering = ['name', 'surname']

    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name="attendees",
        verbose_name='Evento',
        help_text='Evento al que asistió',
        )
    name = models.CharField(
        verbose_name='Nombre',
        help_text='Nombre propio',
        max_length=256,
        )
    surname = models.CharField(
        verbose_name='Apellidos',
        help_text='Apellidos',
        max_length=384,
        )
    email = models.EmailField(
        verbose_name='E-Mail',
        help_text='Correo electrónico al que remitir el certificado',
        max_length=256,
        blank=True,
        null=True,
        default=None,
        )
    uuid = models.UUIDField(
        editable=False,
        default=uuid.uuid4,
        verbose_name='Id. público del certificado',
        )
    pdf = models.FileField(
        max_length=512,
        upload_to=_issued_certificates_upload_to,
        help_text='Generated PDF',
        blank=True,
        null=True,
        default=None,
        )
    issued_at = models.DateTimeField(
        editable=False,
        verbose_name='Fecha de expedición',
        blank=True,
        default=None,
        null=True,
        )

    @classmethod
    def load_attendee(cls, pk: int):
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            return None

    @classmethod
    def load_attendee_by_uuid(cls, uuid):
        try:
            return cls.objects.get(uuid=uuid)
        except cls.DoesNotExist:
            return None

    def full_name(self):
        return f'{self.name} {self.surname}'

    def __str__(self):
        return f'{self.full_name()} asiste a {self.event}'

    def is_issued(self):
        return self.pdf and self.issued_at


def svg_to_pdf(svg_filename, pdf_filename):
    subprocess.run([
        'inkscape',
        svg_filename,
        '--export-area-page',
        f'--export-filename={pdf_filename}',
        ])


def issue_certificate_for_attendee(certificate, attendee):

    if attendee.event != certificate.event:
        raise ValueError(
            f'Certificate {certificate}'
            f'is not available for {attendee}'
            )

    if attendee.pdf:
        if os.path.isfile(attendee.pdf.path):
            os.remove(attendee.pdf.path)
        attendee.uuid = uuid.uuid4()

    data = Context(model_to_dict(attendee))
    data['uuid'] = str(attendee.uuid)
    with open(certificate.template.path, 'r', encoding='utf-8') as f_in:
        template = Template(f_in.read())
    with NamedTemporaryFile(mode='w', encoding='utf-8', suffix=".svg") as f_svg:
        f_svg.write(template.render(data))
        f_svg.flush()
        svg_filename = f_svg.name
        with NamedTemporaryFile(mode='w', encoding='utf-8', suffix=".pdf") as f_pdf:
            pdf_filename = f_pdf.name
            svg_to_pdf(svg_filename, pdf_filename)
            attendee.uuid = uuid.uuid4()
            with open(pdf_filename, 'rb') as doc_file:
                attendee.pdf.save(pdf_filename, File(doc_file), save=True)
                attendee.issued_at = just_now()
                attendee.save()
