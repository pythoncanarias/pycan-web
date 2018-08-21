from django.contrib import admin

from .models import SponsorshipLevel, Sponsor


class SponsorshipLevelAdmin(admin.ModelAdmin):
    pass


admin.site.register(SponsorshipLevel, SponsorshipLevelAdmin)


class SponsorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Sponsor, SponsorAdmin)
