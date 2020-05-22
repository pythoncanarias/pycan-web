from django.contrib import admin

from . import models

# Register your models here.

class JobOfferAdmin(admin.ModelAdmin):
    list_display = (
        "employer",
        "title",
        "salary",
        "approved",
    )


admin.site.register(models.JobOffer, JobOfferAdmin)

