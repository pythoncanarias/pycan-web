from django.contrib import admin

from .models import Social, Speaker, Contact


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    prepopulated_fields = {'code': ('name', ), }


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ), }


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass
