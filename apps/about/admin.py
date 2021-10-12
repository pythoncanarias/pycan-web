from django.contrib import admin

from . import models


@admin.register(models.Ally)
class AllyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'url',
        'twitter',
        'email',
    )
