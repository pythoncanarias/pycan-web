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
    fields = (('description', 'quantity', 'amount'), )
    ordering = ('-amount', )


def set_active(modeladmin, request, queryset):
    queryset.update(active=True)


set_active.short_description = 'Activate selected invoices.'


def set_inactive(modeladmin, request, queryset):
    queryset.update(active=False)


set_inactive.short_description = 'Deactivate selected invoices.'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [
        ConceptInline,
    ]
    list_filter = ('date', 'organization', 'active')
    list_display = ('__str__', 'date', 'organization', 'total', 'active', 'invoice_pdf')

    fields = ('client', 'organization', ('invoice_number', 'active'), 'date', ('taxes', 'retention'))
    readonly_fields = ('invoice_number', )
    ordering = ('-date', )

    actions = [set_active, set_inactive]

    def invoice_pdf(self, invoice):
        if not os.path.isfile(invoice.path):
            invoice.render()

        return mark_safe('<a href="{}" download>Download</a>'.format(invoice.filename_url()))

    invoice_pdf.short_description = 'File Download'
