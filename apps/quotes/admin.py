from django.contrib import admin

from .models import Author, Quote
from .forms import QuoteForm

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class AuthorResource(resources.ModelResource):

    class Meta:
        model = Author
        export_order = ('id',)


@admin.register(Author)
class AuthorAdmin(ImportExportModelAdmin):
    ordering = ['name', 'surname']
    list_display = ('name', 'surname', 'url',)
    search_fields = ['name', 'surname']
    resource_class = AuthorResource


class QuoteResource(resources.ModelResource):

    class Meta:
        model = Quote
        export_order = ('id',)


@admin.register(Quote)
class QuoteAdmin(ImportExportModelAdmin):
    list_display = ('text', 'author',)
    resource_class = QuoteResource
    list_select_related = ('author',)
    list_filter = ('created', 'author')
    search_fields = ['text', 'author__name', 'author__surname']
    form = QuoteForm
