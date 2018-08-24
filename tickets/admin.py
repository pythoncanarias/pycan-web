from django.contrib import admin
from .models import TicketCategory, Article, Ticket


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ), }
