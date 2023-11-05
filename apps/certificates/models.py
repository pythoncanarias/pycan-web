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
