from django.contrib import admin

from .models import Venue, Location


class LocationInline(admin.StackedInline):
    model = Location
    extra = 0


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'locations')
    prepopulated_fields = {'slug': ('name', ), }
    inlines = [LocationInline]

    def locations(self, obj):
        return ", ".join(obj.locations.values_list('name', flat=True))
