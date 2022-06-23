from django.contrib import admin

from . import models


class LabelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(models.Label, LabelAdmin)


class ResourceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'url')
    filter_horizontal = ('labels',)


admin.site.register(models.Resource, ResourceAdmin)
