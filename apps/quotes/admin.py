from django.contrib import admin

from .models import Author, Quote
from .forms import QuoteForm


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    ordering = ['name', 'surname']
    list_display = ('name', 'surname', 'url',)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'author',)
    list_select_related = ('author',)
    list_filter = ('created', 'author')
    form = QuoteForm
