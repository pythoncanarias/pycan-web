from django.contrib import admin

from .models import Social, Speaker, Contact


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    prepopulated_fields = {'code': ('name', ), }
    list_display = ('name', 'code', 'base_url')


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', 'surname'), }
    inlines = [ContactInline]
    search_fields = ['name', 'surname']
    list_display = ('name', 'surname', 'email')
    ordering = ['name', 'surname']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('speaker', 'social', 'href')
    list_filter = ['social']
    search_fields = ['speaker__name', 'speaker__surname']
