#!/usr/bin/env python3

from django.db import models

from apps.events.models import Event


def _certificates_upload_dir(instance, filename):
    return "events/event/{instance.event.pk}/{filename}"


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
        upload_to=_certificates_upload_dir,
        help_text='Template to be used to generate PDF',
    )
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.description)


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

    def __str__(self):
        return f'{self.name} {self.surname} asiste a {self.event}'
