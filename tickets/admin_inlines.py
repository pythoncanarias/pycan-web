from django.contrib import admin
from .models import Article, Gift


class ArticleInline(admin.StackedInline):
    model = Article
    extra = 0


class GiftInline(admin.StackedInline):
    model = Gift
    extra = 0
