from django.contrib import admin

# Register your models here.
from .models import FAQItem

admin.site.register(FAQItem)

"""
# una referencia de pycan:

from . import models


@admin.register(models.Ally)
class AllyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'url',
        'twitter',
        'email',
    )
"""
