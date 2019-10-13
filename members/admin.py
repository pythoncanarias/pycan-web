from django.contrib import admin

from members.models import Member, Position


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass
