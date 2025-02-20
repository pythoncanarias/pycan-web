from django.contrib import admin

from .models import (
    Member,
    Membership,
    Position,
    Role,
)


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0
    classes = ['collapse']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    def active(self, obj):
        return obj.active
    active.boolean = True

    raw_id_fields = ['user']
    list_display = ('full_name', 'user', 'email', 'pk', 'active',
                    'is_founder')
    search_fields = ('id', 'user__first_name', 'user__last_name',
                     'user__email')
    inlines = (MembershipInline, )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    def active(self, obj):
        return obj.active
    active.boolean = True

    raw_id_fields = ['member']
    list_display = ('member', 'role', 'since', 'until', 'active')
    list_filter = ('since', 'until')
    search_fields = ('member__user__first_name', 'member__user__last_name',
                     'member__user__username', 'member__user__email')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    raw_id_fields = ['member']
    list_display = ('member', 'valid_from', 'valid_until', 'fee_amount')
    search_fields = ('member__user__first_name', 'member__user__last_name',
                     'member__user__username', 'member__user__email')
    list_filter = ('fee_amount',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'role_name', 'weight')
