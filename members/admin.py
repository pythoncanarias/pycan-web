from django.contrib import admin

from members.models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
