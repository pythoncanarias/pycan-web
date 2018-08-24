from django.contrib import admin
from .models import TicketCategory, Article, Ticket


class TicketCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(TicketCategory, TicketCategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)


class TicketAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ticket, TicketAdmin)
