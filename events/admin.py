from django.contrib import admin, messages

from .models import Badge, Event, Refund, WaitingList


def render_event_badges(modeladmin, request, queryset):
    prints = []
    for event in queryset:
        prints.append(request.get_host() + event.render_all_badges())
    messages.add_message(request, messages.INFO,
                         f"Generated PDFs in -> {' '.join(prints)} ")


render_event_badges.short_description = "Generate a PDF with all the badges"


@admin.register(Badge)
class BadgeInline(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'hashtag': ('name', ), }
    actions = [render_event_badges]
    list_display = ('name', 'hashtag', 'active',
                    'opened_ticket_sales', 'start_date')


@admin.register(WaitingList)
class WaitingListAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'phone',
        'created_at',
        'fixed_at',
        'buy_code',
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
