from django.contrib import admin
from .models import TicketCategory, Article, Ticket


class ArticleInline(admin.StackedInline):
    model = Article
    extra = 0


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', ), }


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('event', 'category', 'price', 'stock', 'release_at')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('number', 'keycode', 'customer_email',
                    'sold_at', 'article')
