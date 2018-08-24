from django.contrib import admin

from .models import SlotCategory, SlotTag, SlotLevel, Slot, \
    Track, Schedule


@admin.register(SlotCategory)
class SlotCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SlotTag)
class SlotTagAdmin(admin.ModelAdmin):
    pass


@admin.register(SlotLevel)
class SlotLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    pass


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass
