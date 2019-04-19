import os

from django.contrib import admin
from django.utils.safestring import mark_safe

from invoices.models import Client, Concept, Invoice


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_filter = ('city', )
    list_display = ('__str__', 'city')


class ConceptInline(admin.StackedInline):
    model = Concept
    fields = (('description', 'quantity', 'amount'),)
    ordering = ('-amount', )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [ConceptInline, ]
    list_filter = ('date', 'client', 'active')
    list_display = ('__str__', 'date', 'client', 'proforma', 'active', 'taxes',
                    'retention', 'invoice_pdf')

    fields = ('client', ('invoice_number', 'proforma', 'active'), 'date',
              ('taxes', 'retention'))
    readonly_fields = ('invoice_number', )
    ordering = ('-date', )

    def invoice_pdf(self, invoice):
        if not os.path.isfile(invoice.path):
            invoice.render()

        return mark_safe('<a href="{}" download>Download</a>'.format(
            invoice.filename_url()))

    invoice_pdf.short_description = 'File Download'
