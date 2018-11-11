from django.contrib import admin, messages
from .models import Event, Badge
from .models import WaitingList


def render_event_badges(modeladmin, request, queryset):
    prints = []
    for event in queryset:
        prints.append(request.get_host() + event.render_all_badges())
    messages.add_message(request, messages.INFO, f"Generated PDFs in -> {' '.join(prints)} ")


render_event_badges.short_description = "Generate a PDF with all the badges"


class BadgeInline(admin.StackedInline):
    model = Badge
    min_num = 1
    max_num = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [BadgeInline]
    prepopulated_fields = {'slug': ('name', ), }
    actions = [render_event_badges]
    list_display = ('name', 'slug', 'active',
                    'opened_ticket_sales', 'start_date')


@admin.register(WaitingList)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'event',
        'name',
        'surname',
        'email',
        'created_at',
        'fixed_at',
        )

    
