from django.contrib import admin

from members.models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']

    list_display = [
        'full_name',
        'email',
        'is_active',
        'public_membership',
        ]

    def is_active(self, obj):
        return obj.active

    is_active.boolean = True
