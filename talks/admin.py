from django.contrib import admin

from .models import Track, TalkTag, TalkLevel, Talk, Speaker


class TrackAdmin(admin.ModelAdmin):
    pass


admin.site.register(Track, TrackAdmin)


class TalkTagAdmin(admin.ModelAdmin):
    pass


admin.site.register(TalkTag, TalkTagAdmin)


class TalkLevelAdmin(admin.ModelAdmin):
    pass


admin.site.register(TalkLevel, TalkLevelAdmin)


class TalkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Talk, TalkAdmin)


class SpeakerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Speaker, SpeakerAdmin)
