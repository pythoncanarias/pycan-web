from django.contrib import admin

from .models import SlotCategory, SlotTag, SlotLevel, Slot, \
    Track, Schedule


class ScheduleInline(admin.StackedInline):
    model = Schedule
    extra = 0
    autocomplete_fields = ['speaker']


@admin.register(SlotCategory)
class SlotCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'code': ('name', ), }
    list_display = ('name', 'code')


@admin.register(SlotTag)
class SlotTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ), }
    list_display = ('name', 'slug')


@admin.register(SlotLevel)
class SlotLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline]
    list_display = ('name', 'category', 'level', '_tags')

    def _tags(self, obj):
        return ', '.join(tag.name for tag in obj.tags.all())


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
