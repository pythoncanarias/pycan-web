import os
from datetime import date
from decimal import Decimal

from django.conf import settings
from django.db import models

from invoices.constants import RETENTION_CHOICES, RETENTION_MULTIPLIER, TAX_CHOICES, TAX_MULTIPLIER
from invoices.services.invoice_maker import InvoiceMaker


class InvoiceManager(models.Manager):

    def for_year(self, year):
        first_day = date(year, 1, 1)
        last_day = date(year, 12, 31)
        return self.filter(date__gte=first_day, date__lte=last_day)


class Invoice(models.Model):
    date = models.DateField()
    taxes = models.IntegerField(choices=TAX_CHOICES, default=0)
    retention = models.IntegerField(choices=RETENTION_CHOICES, default=0)
    invoice_number = models.IntegerField(blank=True)

    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey('invoices.Client', on_delete=models.CASCADE)

    active = models.BooleanField(default=True)

    objects = InvoiceManager()

    @property
    def concepts_total(self):
        """Calculate the invoice total.

        :return: total amount for invoice
        :rtype: Decimal
        """
        return sum([concept.amount * concept.quantity for concept in self.concept_set.all()]).quantize(Decimal('0.01'))

    @property
    def total(self):
        total = self.concepts_total
        total -= self.concepts_total * RETENTION_MULTIPLIER[self.retention] / 100
        total += self.concepts_total * TAX_MULTIPLIER[self.taxes] / 100

        return total.quantize(Decimal('0.01'))

    @property
    def filename(self):
        return '{}.pdf'.format(self.verbose_invoice_number)

    @property
    def path(self):
        return os.path.join(settings.MEDIA_ROOT, 'invoices', self.filename)

    def filename_url(self):
        media_root = settings.MEDIA_URL
        invoices_uri = 'invoices'
        filename = self.filename
        return '/'.join([media_root, invoices_uri, filename]).replace('//', '/')

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.next_invoice_number()
        self.render()
        return super(Invoice, self).save(*args, **kwargs)

    def next_invoice_number(self):
        year = self.date.year
        invoices_for_year = Invoice.objects.for_year(year).exclude(id=self.id)
        return invoices_for_year.latest('id').invoice_number + 1 if invoices_for_year else 1

    @property
    def verbose_invoice_number(self):
        return '{}{:06d}'.format(str(self.date.year)[-2:], self.invoice_number)

    def render(self):
        invoice_rendered = InvoiceMaker(self)
        return invoice_rendered

    def __str__(self):
        return '{} {}'.format(self.verbose_invoice_number, self.date)
