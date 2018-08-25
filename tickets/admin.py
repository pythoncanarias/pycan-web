from django.contrib import admin
from .models import TicketCategory, Article, Ticket


class ArticleInline(admin.StackedInline):
    model = Article
    extra = 0


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ), }


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass
