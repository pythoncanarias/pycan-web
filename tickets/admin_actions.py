def reset_raffle(modeladmin, request, queryset):
    for raffle in queryset.all():
        raffle.clean_awarded_tickets()
        raffle.closed_at = None
        raffle.save()


reset_raffle.short_description = 'Reset and re-open raffle'
