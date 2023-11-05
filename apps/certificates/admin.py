from django.contrib import admin

from . import models


class CertificateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'description', 'template')
    # filter_horizontal = ('event',)


admin.site.register(models.Certificate, CertificateAdmin)
