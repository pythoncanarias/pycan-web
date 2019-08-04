from django.contrib import admin
from .models import Article, Present


class ArticleInline(admin.StackedInline):
    model = Article
    extra = 0


class PresentInline(admin.StackedInline):
    model = Present
    extra = 0
