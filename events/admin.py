from django.contrib import admin, messages
from .models import Event
from .models import Badge
from .models import WaitingList
from .models import Refund


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
        'full_name',
        'email',
        'phone',
        'created_at',
        'fixed_at',
        )

    def full_name(self, obj):
        return '{}, {}'.format(
            obj.surname,
            obj.name,
            )


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ticket',
        'event',
        'created_at',
        'fixed_at',
        )
