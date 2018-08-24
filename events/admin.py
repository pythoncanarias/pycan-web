from django.contrib import admin

from .models import Event
from organizations.admin import MembershipInline


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ), }
    inlines = [MembershipInline]
