from django.contrib import admin

from .models import Event, Badge


class BadgeInline(admin.StackedInline):
    model = Badge
    min_num = 1
    max_num = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [BadgeInline]
    prepopulated_fields = {'slug': ('name', ), }
    list_display = ('name', 'slug', 'active',
                    'opened_ticket_sales', 'start_date')


