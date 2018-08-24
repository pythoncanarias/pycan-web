from django.contrib import admin

from .models import Venue, Location


class LocationInline(admin.StackedInline):
    model = Location
    extra = 0


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ), }
    inlines = [LocationInline]
