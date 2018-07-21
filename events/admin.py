#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.html import format_html

from .models import Event, TicketType, Ticket

class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event, EventAdmin)


class TicketTypeAdmin(admin.ModelAdmin):
    list_display = (
        'desc', 'price', 'stock',
        'sold_tickets', 'release_at', 'is_active',
        )

    def desc(self, obj):
        return format_html(
                '{} (<i style="color:#CfCfCf">{}</i>)',
            obj.name,
            obj.event.title,
            )

    def sold_tickets(self, obj):
        return '{}/{}'.format(obj.num_sold_tickets, obj.num_available_tickets) 

    sold_tickets.short_description = 'sold/available'

admin.site.register(TicketType, TicketTypeAdmin)


class TicketAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ticket, TicketAdmin)




