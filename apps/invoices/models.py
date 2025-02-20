#!/usr/bin/env python3

import os
from datetime import date as Date
from decimal import Decimal

from django.db import models
from django.conf import settings

from .constants import RETENTION_CHOICES, RETENTION_MULTIPLIER, TAX_CHOICES, TAX_MULTIPLIER
from .services.invoice_maker import InvoiceMaker


class Client(models.Model):
    name = models.CharField(max_length=100)
    nif = models.CharField(max_length=12)
    address = models.CharField(max_length=120)
    rest_address = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=30)
    email = models.EmailField(max_length=150, blank=True, null=True)

    def __str__(self):
        return '{} nif: {}'.format(self.name, self.nif)


class InvoiceManager(models.Manager):

    def for_year(self, year):
        first_day = Date(year, 1, 1)
        last_day = Date(year + 1, 1, 1)
        return self.filter(date__gte=first_day, date__lt=last_day)

    def for_event(self, event):
        return self.filter(event=event)

    def for_organization(self, organization):
        return self.filter(organization=organization)


class Invoice(models.Model):
    date = models.DateField()
    taxes = models.IntegerField(choices=TAX_CHOICES, default=0)
    retention = models.IntegerField(choices=RETENTION_CHOICES, default=0)
    invoice_number = models.IntegerField(blank=True)

    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.PROTECT,
        related_name='invoices',
        null=True,
        )
    active = models.BooleanField(default=True)

    objects = InvoiceManager()

    def concepts_total(self):
        """Calculate the invoice total.

        :return: total amount for invoice
        :rtype: Decimal
        """
        return sum([
            concept.amount * concept.quantity
            for concept in self.concept_set.all()
            ]).quantize(Decimal('0.01'))

    @property
    def total(self):
        total = self.concepts_total()
        total -= self.concepts_total() * RETENTION_MULTIPLIER[self.retention] / 100
        total += self.concepts_total() * TAX_MULTIPLIER[self.taxes] / 100
        return total.quantize(Decimal('0.01'))

    def filename(self):
        return f'{self.verbose_invoice_number()}.pdf'

    def path(self):
        return os.path.join(settings.MEDIA_ROOT, 'invoices', self.filename())

    def filename_url(self):
        media_root = settings.MEDIA_URL
        invoices_uri = 'invoices'
        return '/'.join([media_root, invoices_uri, self.filename()]).replace('//', '/')

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.next_invoice_number()
        self.render()
        return super(Invoice, self).save(*args, **kwargs)

    def next_invoice_number(self):
        year = self.date.year
        invoices_for_year = Invoice.objects.for_year(year).exclude(id=self.id)
        return invoices_for_year.latest('id').invoice_number + 1 if invoices_for_year else 1

    def verbose_invoice_number(self):
        return '{}{:06d}'.format(str(self.date.year)[-2:], self.invoice_number)

    def render(self):
        return InvoiceMaker(self)

    def __str__(self):
        return f'{self.verbose_invoice_number()} {self.date}'


class Concept(models.Model):

    description = models.CharField(max_length=120)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)
        self.invoice.save()
        return obj

    def __str__(self):
        return self.description
