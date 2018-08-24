from django.contrib import admin

from .models import SlotCategory, SlotTag, SlotLevel, Slot, \
    Track, Schedule


class ScheduleInline(admin.StackedInline):
    model = Schedule
    extra = 0


@admin.register(SlotCategory)
class SlotCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'code': ('name', ), }


@admin.register(SlotTag)
class SlotTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ), }


@admin.register(SlotLevel)
class SlotLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass
