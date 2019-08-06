from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from import_export.admin import ImportExportActionModelAdmin

from certificates.utils import create_certificate
from events.tasks import send_ticket

from .admin_inlines import ArticleInline, GiftInline
from .models import Article, Gift, Raffle, Ticket, TicketCategory


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name', ), }


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = ['event']
    list_display = (
        'event', 'category', 'price', 'stock',
        'sold_vs_available',
        'release_at', 'is_active',
        )

    def sold_vs_available(self, obj):
        return "{}/{}".format(
            obj.num_sold_tickets,
            obj.num_available_tickets,
            )


@admin.register(Ticket)
class TicketAdmin(ImportExportActionModelAdmin):
    list_display = (
        'customer_email', 'full_name', 'number',
        'sold_at', 'is_mail_send'
        )
    search_fields = (
        'customer_email',
        'customer_name',
        'customer_surname',
        'keycode',
        'number',
        )
    ordering = ('-sold_at', '-number')
    list_filter = ('article', 'sold_at', )

    def full_name(self, obj):
        return "{}, {}".format(
            obj.customer_surname,
            obj.customer_name,
            )

    def is_mail_send(self, obj):
        return bool(obj.sold_at)

    is_mail_send.boolean = True

    def resend_ticket_force(self, request, queryset):
        for ticket in queryset:
            send_ticket.delay(ticket, force=True)

    resend_ticket_force.short_description = "Recreate and send ticket"

    def resend_ticket(self, request, queryset):
        for ticket in queryset:
            send_ticket.delay(ticket)

    resend_ticket.short_description = "Resend ticket"

    def download_emails(self, request, queryset):
        distinct_emails = queryset.order_by().values_list(
            'customer_email', flat=True).distinct()
        content = ','.join(distinct_emails)
        filename = 'emails.txt'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={}'.format(
            filename)
        return response

    download_emails.short_description = "Download customers' emails"

    def gen_certificate(self, request, queryset):
        for ticket in queryset:
            create_certificate(
                'attendance',
                output_name=ticket.keycode,
                name=ticket.customer_full_name,
                )

    gen_certificate.short_description = 'Generar certificado de asistencia'

    actions = [
        resend_ticket,
        resend_ticket_force,
        download_emails,
        gen_certificate,
        ]


@admin.register(Raffle)
class RaffleAdmin(admin.ModelAdmin):
    inlines = [GiftInline]
    list_display = [
        'event', 'is_opened', 'delivered_vs_total_gifts', 'created_at',
        'raffle_url'
    ]

    def raffle_url(self, obj):
        return format_html(
            f'<a href="{obj.get_absolute_url()}">{obj.get_absolute_url()}</a>')

    def delivered_vs_total_gifts(self, obj):
        return f'{obj.get_delivered_gifts().count()}/{obj.gifts.count()}'

    def is_opened(self, obj):
        return obj.opened
    is_opened.short_description = 'opened'
    is_opened.boolean = True


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ['name', 'awarded_participant', 'awarded_at', 'raffle']
    list_filter = ('raffle',)
    exclude = ('missing_tickets',)

    def awarded_participant(self, obj):
        if obj.awarded_ticket:
            return obj.awarded_ticket.customer_full_name
        else:
            return None
