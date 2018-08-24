from django.contrib import admin

from .models import Social, Speaker, Contact


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    prepopulated_fields = {'code': ('name', ), }


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ), }
    inlines = [ContactInline]
    search_fields = ['name', 'surname']
