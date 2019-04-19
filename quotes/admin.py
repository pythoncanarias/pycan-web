from django.contrib import admin

from .models import Author, Quote


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'url',)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'author',)
