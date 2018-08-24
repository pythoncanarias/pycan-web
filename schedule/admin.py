from django.contrib import admin

from .models import SlotCategory, SlotTag, SlotLevel, Slot, \
    Track, Schedule


class SlotCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(SlotCategory, SlotCategoryAdmin)


class SlotTagAdmin(admin.ModelAdmin):
    pass


admin.site.register(SlotTag, SlotTagAdmin)


class SlotLevelAdmin(admin.ModelAdmin):
    pass


admin.site.register(SlotLevel, SlotLevelAdmin)


class SlotAdmin(admin.ModelAdmin):
    pass


admin.site.register(Slot, SlotAdmin)


class TrackAdmin(admin.ModelAdmin):
    pass


admin.site.register(Track, TrackAdmin)


class ScheduleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Schedule, ScheduleAdmin)
