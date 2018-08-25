from django.contrib import admin

from .models import Event
from organizations.admin import MembershipInline
from schedule.admin import ScheduleInline
from tickets.admin import ArticleInline


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ), }
    inlines = [MembershipInline, ScheduleInline, ArticleInline]
    list_display = ('name', 'slug', 'active',
                    'opened_ticket_sales', 'start_date')
