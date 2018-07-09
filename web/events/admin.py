#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Event, TicketType, Ticket

class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event, EventAdmin)


class TicketTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(TicketType, TicketTypeAdmin)


class TicketAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ticket, TicketAdmin)




