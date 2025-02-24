from django.contrib import admin

from . import models


class CertificateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'description', 'template')


admin.site.register(models.Certificate, CertificateAdmin)


class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'surname', 'certificate', 'is_issued')


admin.site.register(models.Attendee, AttendeeAdmin)
