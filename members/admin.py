from django.contrib import admin

from members.models import Member, Position, Membership


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    list_display = ('full_name', 'user', 'email', 'member_id')
    search_fields = ('id', 'user__first_name', 'user__last_name',
                     'user__email')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    pass
