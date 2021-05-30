from django.contrib import admin

from .models import NoticeKind, Notice


@admin.register(NoticeKind)
class NoticeKindAdmin(admin.ModelAdmin):
    list_display = ('pk', 'app', 'code', 'description',)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'kind_id',
        'member_id',
        # 'reference_date',
        # 'is_sent',
    )
    list_filter = (
        'kind',
        'member',
    )
