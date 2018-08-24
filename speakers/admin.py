from django.contrib import admin

from .models import Social, Speaker, Contact


class SocialAdmin(admin.ModelAdmin):
    pass


admin.site.register(Social, SocialAdmin)


class SpeakerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Speaker, SpeakerAdmin)


class ContactAdmin(admin.ModelAdmin):
    pass


admin.site.register(Contact, ContactAdmin)
