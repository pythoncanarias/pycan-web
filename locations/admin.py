from django.contrib import admin

from .models import Venue, Location


class VenueAdmin(admin.ModelAdmin):
    pass


admin.site.register(Venue, VenueAdmin)


class LocationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Location, LocationAdmin)
