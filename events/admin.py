from django.contrib import admin

from .models import Event



@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ), }
    list_display = ('name', 'slug', 'active',
                    'opened_ticket_sales', 'start_date')


