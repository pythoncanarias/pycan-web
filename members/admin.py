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
    raw_id_fields = ['member']
    list_display = ('member', 'position', 'since', 'until', 'active')
    list_filter = ('active', 'since', 'until')
    search_fields = ('member__user__first_name', 'member__user__last_name',
                     'member__user__username', 'member__user__email')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    raw_id_fields = ['member']
    list_display = ('member', 'member_category', 'valid_from', 'valid_until',
                    'fee_amount')
    search_fields = ('member__user__first_name', 'member__user__last_name',
                     'member__user__username', 'member__user__email')
    list_filter = ('member_category', 'fee_amount')
